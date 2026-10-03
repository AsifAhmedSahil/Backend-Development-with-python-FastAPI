from fastapi import FastAPI


app = FastAPI(title="Hospital management system")


@app.get("/")
async def root():
    return {"message":"Welcome to the hospital management system API!"}
    
