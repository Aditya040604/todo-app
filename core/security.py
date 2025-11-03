from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


SECRET_KEY = "b2e062c10c6d21899c5074540ff1b35aac93a7acb7b434b93c945f902fd9e84f"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta):
    payload = data.model_dump().copy()
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
