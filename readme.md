# 🚀 FastAPI Backend Development — Learning Journey

A hands-on collection of **FastAPI** projects demonstrating core backend concepts: CRUD operations, path & query parameters, request validation with Pydantic, and a loan risk prediction API.

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

## 🔍 Pydantic Validation — How It Works in This Code

### Definition (in `dtos.py` & `loan.py`)

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
```

### How It Works (step by step)

1. Client sends `POST /predict` with JSON body:
   ```json
   {"age": 30, "income": 60000, "loan_amount": 500000, "employment_years": 5}
   ```
2. FastAPI reads the request body and passes it to Pydantic's `LoanApplication` model.
3. Pydantic **automatically**:
   - Validates types (`age` must be `int`, `income` must be `float`, etc.)
   - Provides default values (e.g. `count: int = 0` — uses 0 if not sent)
   - Raises `ValidationError` with a clear message if types are wrong
4. If validation passes, the function receives a fully-typed Python object.
5. If validation fails → FastAPI returns **422 Unprocessable Entity** with details.

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

---

## 🛠️ How to Run

```bash
# Install fastapi + uvicorn
pip install fastapi uvicorn

# Run any file (e.g. loan.py)
uvicorn fastapi-project.loan:app --reload

# Visit: http://127.0.0.1:8000/docs
```

---

## 📌 What's Next?

- [ ] Refactor into a single app with `APIRouter`
- [ ] Add database (SQLite + SQLAlchemy)
- [ ] Add authentication
- [ ] Write unit tests with `pytest` + `TestClient`
