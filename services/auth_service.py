from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.models import Users
from datetime import timedelta




from core.security import create_access_token, decode_access_token
from schemas.auth_schemas import Payload


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, create_user_request):
        create_user_model = Users(
            email=create_user_request.email,
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            hashed_password=self.bcrypt_context.hash(create_user_request.password),
            role=create_user_request.role,
            is_active=True,
        )
        self.db.add(create_user_model)
        self.db.commit()
    
    def hash_password(self, password: str) -> str:
        return self.bcrypt_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.bcrypt_context.verify(password, hashed_password)

    def create_access_token(self, data: Payload, expires_delta: timedelta) -> dict:
        return create_access_token(data, expires_delta)
    def decode_access_token(self,token:str )-> dict:
        return decode_access_token(token)

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(Users).filter(Users.username == username).first()
        if not user:
            return False
        return user if self.verify_password(password, user.hashed_password) else False
