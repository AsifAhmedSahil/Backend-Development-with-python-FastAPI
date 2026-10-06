from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from app.config import settings
from jose import jwt 

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str,hashed:str) -> bool:
    return pwd_context.verify(plain,hashed)


def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.jwt_secret_key,algorithm=settings.jwt_algorithm)

