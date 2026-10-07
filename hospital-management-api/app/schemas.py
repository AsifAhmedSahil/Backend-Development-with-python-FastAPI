from pydantic import BaseModel,ConfigDict

from datetime import datetime


class PatientCreate(BaseModel):
    name:str
    age:int
    gender:str
    contract_number:str
    diagnosis:str
    doctor_assigned:str


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    name:str
    age:int
    gender:str
    contract_number:str
    diagnosis:str
    doctor_assigned:str
    admitted_at:datetime


class StaffCreate(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str = "bearer"

    