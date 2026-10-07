from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import StaffCreate,Token
from app.auth import hash_password,verify_password,create_access_token
from app.database import get_db
from sqlalchemy import select
from app.models import Patient,Stuff
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/staff",tags=["staff"])

@router.post("/signup")
async def signup(staff:StaffCreate,db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stuff).where(Stuff.email == staff.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400,detail="Email already registered")
    new_staff = Stuff(email=staff.email,hashed_password=hash_password(staff.password))

    db.add(new_staff)
    await db.commit()
    return {"message":"Staff account created successfully"}

@router.post("/login",response_model=Token)
async def login(from_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stuff).where(Stuff.email == from_data.username))
    staff = result.scalar_one_or_none()
    if not staff or not verify_password(from_data.password,staff.hashed_password):
        raise HTTPException(status_code=400,detail="Invalid credentials")
    token = create_access_token(data={"sub":staff.email})
    return Token(access_token=token)
