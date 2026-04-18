# import fastapi

# print(fastapi.__version__)

from fastapi import FastAPI ,Request
from mockData import products

app = FastAPI()

@app.get("/")
def home():
    return "Welcome Home"

@app.get("/contact")
def contact():
    return "contact us!"

@app.get("/products")
def get_products():
    return products

# path params

@app.get("/product/{product_id}")
def get_one_product(product_id:int):
    for oneProduct in products:
        if oneProduct.get("id") == product_id:
            return oneProduct

    return {
        "error":"Product not found in database"
    }


# Query parameter 

# @app.get("/greet")
# def greet(name:str,age:int):
#     return {
#         "greet":f"Hello {name}. Your age is {age}"
#     }

# Query parameter with all request in one

@app.get("/greetuser")
def greet_user(request:Request):
    
    query_params = dict(request.query_params)
    print(query_params)
    return {
        "greet":f"Hello {query_params.get("name")}. Your age is {query_params.get("age")}"
    }
