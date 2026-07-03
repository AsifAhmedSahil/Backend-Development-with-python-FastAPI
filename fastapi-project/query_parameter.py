from fastapi import FastAPI

app = FastAPI()

all_customers = [
    {"id":101,"name":"asif","city":"ctg","risk":"low"},
    {"id":102,"name":"asif2","city":"dhk","risk":"high"},
    {"id":103,"name":"asif3","city":"ctg","risk":"low"},
    {"id":104,"name":"asif4","city":"cum","risk":"low"}
]

@app.get("/customers")
def get_customers(city:str,risk:str):
    filtered = [
        c for c in all_customers
        if c["city"] == city and c["risk"] == risk
    ]

    return {
        "city":city,
        "risk":risk,
        "count":len(filtered),
        "Results":filtered
    }