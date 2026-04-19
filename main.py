# import fastapi

# print(fastapi.__version__)

from fastapi import FastAPI ,Request
from mockData import products
from dtos import productDTO

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


# pydantic validation and create api
@app.post("/create-product")
def create_product(product_data:productDTO):
    print(product_data)
    # convert pydentic data to dictionary
    product_data = product_data.model_dump()
    print(product_data)

    products.append(product_data)

    return {"status":"Product created successfully...","data" : products}

@app.put("/update-product/{product_id}")
def update_product(product_data:productDTO,product_id:int):
    for index,oneProduct in enumerate(products):
        if oneProduct.get("id") == product_id:
            products[index] = product_data.model_dump()
            return {"status":"product updated successfully","data":product_data}
    
    return {
        "error":"Product not found in database in this id"
    }

@app.delete("/delete_product/{produce_id}")
def delete_product(produce_id: int):
    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == produce_id:
            deleted_product = products.pop(index)
            return {
                "status": "Product deleted successful",
                "product": deleted_product
            }

    return {
        "error": "Product not found in database in this id"
    }