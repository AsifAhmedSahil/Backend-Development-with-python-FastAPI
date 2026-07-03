from fastapi import FastAPI

app = FastAPI()

customer_risk_profile = {
    101:{"name":"asif","risk":"low","score":0.15},
    102:{"name":"ahmed","risk":"high","score":0.15},
    103:{"name":"sahil","risk":"low","score":0.15},
}
# with curly bracket parameter = query parameter
@app.get("/customers")
def get_customers(city:str,risk:str):
    return {"city":city,"risk":risk}


# parameter with curly bracket
@app.get("/customer/{customer_id}")
def get_customer_risk(customer_id:int):
    if customer_id not in customer_risk_profile:
        return {"error":f"customer {customer_id} not found"}
    profile = customer_risk_profile[customer_id]

    return {
        "customer_id":customer_id,
        "name":profile["name"],
        "risk":profile["risk"],
        "score":profile["score"]
    }

    