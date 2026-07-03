from fastapi import FastAPI

app = FastAPI()

# server chalanor jonno ruin:  uvicorn main:app --reload

@app.get("/")
def home():
    return {"message":"this is home page"}

@app.get("/about")
def about():
    return {"project":"Load risk model","version":"1.0"}

