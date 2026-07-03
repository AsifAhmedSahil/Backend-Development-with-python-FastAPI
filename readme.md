# 🚀 FastAPI Backend Development — Learning Journey

A hands-on collection of **FastAPI** projects demonstrating core backend concepts: CRUD operations, path & query parameters, request validation with Pydantic, and a loan risk prediction API.

---

## 📁 Project Structure

```
Backend-Development-with-python-FastAPI/
├── main.py                        # Product CRUD API (root level)
├── dtos.py                        # Pydantic DTO for product validation
├── mockData.py                    # Mock product database
├── fastapi-project/               # Loan & Customer Risk API
│   ├── main.py                    # Basic routes (/, /about)
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

## 🧪 Small Interview Questions (based on this code)

| # | Question | Answer |
|---|----------|--------|
| 1 | What's the difference between **path parameter** and **query parameter**? | Path: `/customer/101` — part of URL route. Query: `/customers?city=ctg` — key-value after `?`. Path for identity, query for filtering. |
| 2 | Why does `predict_loan` return only `age` and `decision`, not all fields? | The response dict explicitly picks fields — you control what the API returns, not required to send everything. |
| 3 | What happens if I send `POST /predict` with `income: "fifty thousand"` (string)? | Pydantic's `BaseModel` validates types → FastAPI returns **422 Validation Error** before reaching the function. |
| 4 | How would you make `city` parameter optional in `/customers`? | Use `Optional[str] = None` from `typing` and handle the `None` case in filter logic. |
| 5 | What's the issue with having **multiple FastAPI apps** (one per file)? | Each file creates its own `app = FastAPI()` — they can't run together. Better to use `APIRouter` or a single app with imports. |

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
