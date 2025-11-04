from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from core.config import settings



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    payload = data.model_dump().copy()
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
