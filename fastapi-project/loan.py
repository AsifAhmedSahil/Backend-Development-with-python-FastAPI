from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    age:int
    income: float
    load_amount: float
    employeement_years:int


@app.post("/predict")
def predict_loan(application: LoanApplication):

    if application.income > 50000 and application.employeement_years > 2:
        decision = "approved"
    else:
        decision = "rejected"

    return {
        "application_age":application.age,
        "decision":decision
    }
