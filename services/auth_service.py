from models.models import Users
from datetime import timedelta
from fastapi import HTTPException
from starlette import status

from repositories.user_repo import UserRepository
from core.security import create_access_token, decode_access_token
from schemas.auth_schemas import Payload
from core.security import verify_password


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_access_token(self, data: Payload, expires_delta: timedelta) -> dict:
        return create_access_token(data, expires_delta)
    def decode_access_token(self,token:str )-> dict:
        return decode_access_token(token)

    def verify_access_token(self, token:str) -> int:
        payload = self.decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return int(user_id)

    def get_current_user(self, token:str) -> Users:
        user_id = self.verify_access_token(token)

        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
        return user

    
    def authenticate_user(self, username: str, password: str) -> str:
        user = self.repo.get_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        data = Payload(user_name=user.username, user_id=user.id, user_role=user.role)
        token = self.create_access_token(data, timedelta(minutes=30))
        return token