from pydantic import BaseModel

class productDTO(BaseModel):
    id : int
    title : str
    count : int = 0
    price : int = 0