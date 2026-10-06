from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from app.config import settings
from app.models import Patient,Stuff
from jose import jwt ,JWTError
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/staff/login")


def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str,hashed:str) -> bool:
    return pwd_context.verify(plain,hashed)


def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.jwt_secret_key,algorithm=settings.jwt_algorithm)

async def get_current_staff(
        token:str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")

    try:
        payload = jwt.decode(token,settings.jwt_secret_key,algorithms=[settings.jwt_algorithm])

        email = payload.get("sub")

    except JWTError:
        raise error
    if email is None:
        raise error
    result = await db.execute(select(Stuff).where(Stuff.email == email))
    staff = result.scalar_one_or_none()
    if staff is None:
        raise error
    return staff
    
