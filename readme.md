# 🚀 FastAPI Backend Development — Learning Journey

A hands-on collection of **FastAPI** projects demonstrating core backend concepts: CRUD operations, path & query parameters, request validation with Pydantic, loan risk prediction, and a California housing price ML model.

---

## 📁 Project Structure

```
Backend-Development-with-python-FastAPI/
├── main.py                        # Product CRUD API (root level)
├── dtos.py                        # Pydantic DTO for product validation
├── mockData.py                    # Mock product database
├── fastapi-project/               # Loan, Student & Customer Risk APIs
│   ├── main.py                    # Basic routes (/, /about)
│   ├── main_s.py                  # Student marks API with HTTPException
│   ├── loan.py                    # Loan approval prediction
│   ├── path_parameter.py          # Path & query params demo
│   └── query_parameter.py         # Filtered customer lookup
├── house-prediction-api/          # ML: California housing price prediction
│   ├── main.py                    # Inference API (load model → predict)
│   ├── train.py                   # Train RandomForest model
│   ├── explore.py                 # Explore dataset
│   ├── house_model.joblib         # Trained model file
│   └── house_features.joblib      # Feature column names
├── task-management/               # Task management with DB migrations
└── README.md
```

---

## ⚙️ fastapi-project — Code Flow

### 1. Basic Routes (`main.py`)

```python
@app.get("/")        # → {"message": "this is home page"}
@app.get("/about")   # → {"project": "Load risk model", "version": "1.0"}
```

**Flow:** Client hits `/` or `/about` → FastAPI matches route → returns JSON response.

---

### 2. Loan Approval Prediction (`loan.py`)

```python
@app.post("/predict")
def predict_loan(application: LoanApplication):
    # Rule: income > 50000 AND employment > 2 years → approved
    # Otherwise → rejected
```

**Flow:** Client sends `POST /predict` with JSON body → Pydantic validates fields (`age`, `income`, `loan_amount`, `employment_years`) → business logic decides **approved / rejected** → returns result.

---

### 3. Path Parameters (`path_parameter.py`)

```python
@app.get("/customer/{customer_id}")
def get_customer_risk(customer_id: int):
    # Looks up customer_risk_profile dict
    # Returns profile or error if not found
```

**Flow:** Client hits `/customer/101` → `customer_id` extracted from URL path → looked up in-memory dict → risk profile returned.

Also demonstrates **query parameters**:

```python
@app.get("/customers")
def get_customers(city: str, risk: str):
    # ?city=ctg&risk=low
```

---

### 4. Filtered Query Parameters (`query_parameter.py`)

```python
@app.get("/customers")
def get_customers(city: str, risk: str):
    # Filters customer list by city AND risk
```

**Flow:** `GET /customers?city=ctg&risk=low` → filter list comprehension → returns matching customers + count.

---

### 5. Student Marks API with Error Handling (`main_s.py`)

**Intuition:** Shows **real-world input validation + HTTPException** — 3 different checks before updating data.

```python
@app.get("/student/{student_id}")
def get_student(student_id: str):
    if student_id not in students:
        raise HTTPException(404, detail=f"student {student_id} does not exist")
    return students[student_id]

@app.post("/student-info")
def add_student(submission: MarksSubmission):
    # Guard 1: Student doesn't exist → 404
    # Guard 2: Marks out of 0-100 range → 400
    # Guard 3: Subject name is empty → 400
    # On success: update marks, return confirmation
```

**Flow:** `POST /student-info` with JSON `{student_id, marks, subject}` → Pydantic validates types → 3 **manual business-rule guards** (`HTTPException`) → update student record → return success.

**Key patterns to remember:**
- `HTTPException(status_code, detail)` — FastAPI's standard error response
- **400** = client sent bad data, **404** = resource not found, **500** = server error
- Business validation (marks 0–100, non-empty subject) happens **after** Pydantic type validation
- Error `detail` can be a **string** or a **dict** with structured info

---

## 🤖 house-prediction-api — ML Model Training

### Dataset: California Housing
Built-in sklearn dataset with ~20K records and 8 features (`MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude`, `Longitude`).

### Code Flow (`train.py`)

```
Load California Housing dataset
        ↓
Convert to DataFrame (X = features, y = target price)
        ↓
train_test_split(80% train, 20% test, random_state=42)
        ↓
Train RandomForestRegressor(n_estimators=100)
        ↓
Predict on test set → Evaluate (MAE, R²)
        ↓
Save model + feature names with joblib
```

### Intuition

```python
# X = input features (e.g. income, house age, rooms)
X = pd.DataFrame(data.data, columns=data.feature_names)

# y = what we want to predict (house price in $100K units)
y = data.target

# 80% data trains the model, 20% tests accuracy
X_train, X_test, Y_train, Y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# RandomForest = many decision trees voting together
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, Y_train)      # learns patterns from training data

y_pred = model.predict(X_test)   # predict on unseen data
mae = mean_absolute_error(Y_test, y_pred)   # avg error ≈ $45K–55K
r2 = r2_score(Y_test, y_pred)               # ~0.80 = good fit

joblib.dump(model, "house_model.joblib")        # save for later use
joblib.dump(list(x.columns), "house_features.joblib")  # save column order
```

### Why This Matters for an API
The saved `.joblib` files are loaded in `main.py` to serve predictions via FastAPI — send house features as JSON → model predicts price → return formatted response.

### Key Concepts
- **`train_test_split`** — prevents data leakage; model never sees test data during training
- **`random_state=42`** — ensures reproducible results every run
- **`n_estimators=100`** — more trees = better accuracy, but slower training
- **`MAE`** — average dollar error (easier to explain to business)
- **`R²`** — how much variance the model explains (0.80 = 80%)
- **`joblib.dump`** — serializes trained model to disk for inference API

---

## 🚀 house-prediction-api — Inference API (`main.py`)

### Startup — Load Model Once
```python
model = joblib.load("house_model.joblib")       # trained RandomForest
features = joblib.load("house_features.joblib")  # column names
```
Model loads **when the app starts** — not on every request. This keeps prediction fast.

### Input Schema — Pydantic with Field Validators
```python
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0)         # must be > 0
    HouseAge: float = Field(ge=0)       # >= 0
    AveRooms: float = Field(gt=0)
    AveBedrms: float = Field(gt=0)
    Population: float = Field(gt=0)
    AveOccup: float = Field(gt=0)
    Latitude: float = Field(ge=32, le=42)     # California bounds
    Longitude: float = Field(ge=-125, le=-114)
```

**New here:** `Field(gt=0, ge=0, le=42)` — Pydantic **range validation** at the schema level, no manual `if` checks needed.

### Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home — API status info |
| `/health` | GET | Health check — shows model name, features, avg error |
| `/predict` | POST | Send 8 house features → get predicted price |

### Prediction Flow (`POST /predict`)
```
Client sends JSON with 8 features
        ↓
Pydantic validates types + ranges (Field constraints)
        ↓
Convert Pydantic model → pandas DataFrame (1 row)
        ↓
model.predict(df) → raw price (in $100K units)
        ↓
Convert to USD (× 100,000) + format with confidence range
        ↓
Return: predicted_price, confidence_range
```

**Intuition:**
```python
# Convert validated input to DataFrame (same column order as training)
input_data = pd.DataFrame([{
    "MedInc": house.MedInc,
    "HouseAge": house.HouseAge,
    ...
}])

# Predict (returns array, take first element)
predicted = model.predict(input_data)[0]   # e.g. 2.15 (=$215K)

# confidence_range uses MAE from training (~$39K)
# "confidence_range": "$176,000 to $254,000"
```

### Key Patterns
- **Model loaded once at module level** — not inside the function (avoids reloading on every request)
- **`Field(gt=, ge=, le=)`** — zero-code range validation, auto-generated in Swagger UI
- **`HTTPException(500)`** — catches prediction errors gracefully
- **Confidence range** — uses training MAE to give a practical price bracket

---

## 🔍 Pydantic Validation — How It Works in This Code

### Definition (across all files)

```python
# dtos.py (root level)
class productDTO(BaseModel):
    id: int
    title: str
    count: int = 0
    price: int = 0

# loan.py (fastapi-project)
class LoanApplication(BaseModel):
    age: int
    income: float
    loan_amount: float        # typo in field name! ("load" in original)
    employment_years: int

# main_s.py (fastapi-project)
class MarksSubmission(BaseModel):
    student_id: str
    marks: int
    subject: str

# house-prediction-api/main.py
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0)         # > 0
    HouseAge: float = Field(ge=0)       # >= 0
    AveRooms: float = Field(gt=0)
    AveBedrms: float = Field(gt=0)
    Population: float = Field(gt=0)
    AveOccup: float = Field(gt=0)
    Latitude: float = Field(ge=32, le=42)     # California bounds
    Longitude: float = Field(ge=-125, le=-114)
```

### How It Works (step by step)

**For basic models** (`productDTO`, `LoanApplication`, `MarksSubmission`):
1. Client sends JSON body → FastAPI passes it to Pydantic model
2. Pydantic validates **types** (age must be int, income must be float, etc.)
3. Provides **default values** (e.g. `count: int = 0`)
4. Raises **422 Validation Error** if types are wrong
5. Validated object is passed to your function

**With `Field()` validators** (`HouseFeatures`):
- `gt=0` → rejects 0 or negative values (e.g. `MedInc: 0` fails)
- `ge=32, le=42` → enforces geographic bounds for California
- All constraints appear automatically in Swagger UI (`/docs`)

**On validation failure** → FastAPI returns **422 Unprocessable Entity** with details.

### Why Pydantic Is Needed

| Benefit | In this code |
|---------|-------------|
| **Type safety** | Ensures `income` is a number, not a string like `"fifty thousand"` |
| **Automatic error messages** | No manual `if not isinstance(...)` checks |
| **IDE autocomplete** | `application.income` gets intellisense in editors |
| **Default values** | `count: int = 0` — field is optional, defaults to 0 |
| **JSON Schema generation** | Powers the `/docs` Swagger UI auto-form |
| **Serialization** | `.model_dump()` converts back to dict for storage/response |

---

## 🧪 Small Interview Questions (based on this code)

| # | Question | Answer |
|---|----------|--------|
| 1 | What's the difference between **path parameter** and **query parameter**? | Path: `/customer/101` — part of URL route. Query: `/customers?city=ctg` — key-value after `?`. Path for identity, query for filtering. |
| 2 | Why does `predict_loan` return only `age` and `decision`, not all fields? | The response dict explicitly picks fields — you control what the API returns, not required to send everything. |
| 3 | What happens if I send `POST /predict` with `income: "fifty thousand"` (string)? | Pydantic's `BaseModel` validates types → FastAPI returns **422 Validation Error** before reaching the function. |
| 4 | What is Pydantic and why is it used with FastAPI? | Pydantic is a data validation library using Python type hints. It ensures request data has correct types, provides clear error messages, generates OpenAPI schema for Swagger docs, and gives IDE autocomplete — all with zero manual validation code. |
| 5 | In `loan.py`, what would happen if `age` is sent as a string `"30"`? | Pydantic tries **type coercion** — `"30"` (str) can be converted to `30` (int), so it would pass. But `"thirty"` cannot, so it returns **422**. |
| 6 | How does `.model_dump()` work in the create-product endpoint? | It converts the Pydantic model instance back to a plain dict so it can be appended to the `products` list and stored/serialized as JSON. |
| 7 | How would you make `city` parameter optional in `/customers`? | Use `Optional[str] = None` from `typing` and handle the `None` case in filter logic. |
| 8 | What's the issue with having **multiple FastAPI apps** (one per file)? | Each file creates its own `app = FastAPI()` — they can't run together. Better to use `APIRouter` or a single app with imports. |
| 9 | What is `HTTPException` and when to use it? | FastAPI's built-in way to return error responses with proper status codes. Use it for any error the client should know about — invalid input (400), missing resource (404), unauthorized (401), etc. |
| 10 | Why does `main_s.py` use 3 separate `if` checks instead of 1? | **Separation of concerns** — each check returns a different status code (400 vs 404) and specific error message. Mixing them would lose clarity. |
| 11 | What's the difference between Pydantic validation and manual `if` checks in `main_s.py`? | Pydantic catches **type errors** (e.g. marks="abc") automatically with 422. Manual checks handle **business rules** (e.g. marks must be 0–100) — Pydantic can't know your domain logic. |
| 12 | In `main_s.py`, why is `marks` validated as 0–100 manually instead of using Pydantic? | Pydantic's `Field(ge=0, le=100)` could do this, but manual `if` checks allow custom error message **with the received value** (`marks_received`) and a **fix hint** — better UX. |
| 13 | What does `train_test_split(X, y, test_size=0.2)` do? | Shuffles the data and splits it: 80% for training (`X_train`, `Y_train`), 20% for testing (`X_test`, `Y_test`). The model never sees test data during training, giving an honest accuracy score. |
| 14 | Why use `random_state=42` in ML? | Makes the random shuffle **deterministic** — every run produces the same split. Without it, you'd get different results each time, making debugging impossible. |
| 15 | What is `RandomForestRegressor` in simple terms? | It creates **100+ decision trees**, each trained on a random subset of data. The final prediction is the **average of all trees** — like asking 100 experts and taking the average. |
| 16 | What's the difference between MAE and R² score? | **MAE** = average dollar error (e.g. "our predictions are off by ~$50K"). **R²** = how well the model explains variance (0.80 = 80% of price changes are explained by the features). |
| 17 | Why save model with `joblib` instead of `pickle`? | `joblib` is more **efficient for large numpy arrays** (common in sklearn models). It compresses better and is faster for scikit-learn objects. |
| 18 | How would you serve this model via FastAPI? | Load `house_model.joblib` + `house_features.joblib` at startup. Create a Pydantic schema for the 8 input features. `POST /predict` → validate → convert to DataFrame → `model.predict()` → return price. |
| 19 | In `house-prediction-api/main.py`, why load model at module level instead of inside the function? | Loading inside the function would **reload the model on every request** — slow and wasteful. Module-level loading runs once at startup. |
| 20 | What does `Field(gt=0, ge=0, le=42)` do? | **Range validation at the schema level** — `gt` = greater than, `ge` = greater/equal, `le` = less/equal. Rejects bad data before the function runs, with auto-generated Swagger docs. |
| 21 | Why is the predicted price multiplied by 100,000? | The California Housing dataset stores prices in **$100K units** (e.g. 2.15 = $215,000). Multiply by 100,000 to get actual USD for readability. |
| 22 | What's the purpose of the `/health` endpoint? | A **readiness probe** — tells clients/monitoring that the API is up, which model is loaded, and what features it expects. Useful for container orchestration (Kubernetes). |
| 23 | Why convert Pydantic model to DataFrame before `model.predict()`? | sklearn models expect **2D array-like input** (rows × columns). A DataFrame preserves column names and order matching the training data — raw dict would fail. |

---

## 🛠️ How to Run

```bash
# Install dependencies
pip install fastapi uvicorn scikit-learn pandas pydantic

# Run FastAPI apps
uvicorn fastapi-project.loan:app --reload           # Loan prediction
uvicorn house-prediction-api.main:app --reload      # House price prediction

# Train ML model first (if model file missing)
cd house-prediction-api
python train.py

# Visit Swagger docs
# http://127.0.0.1:8000/docs
```

---

## 📌 What's Next?

- [ ] Refactor into a single app with `APIRouter`
- [ ] Add database (SQLite + SQLAlchemy)
- [ ] Add authentication
- [ ] Write unit tests with `pytest` + `TestClient`
