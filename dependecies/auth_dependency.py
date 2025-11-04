from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import get_db
from typing import Annotated
from fastapi import Depends

from services.auth_service import AuthService
from services.user_service import UserService
from repositories.user_repo import UserRepository
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION}/auth/token")

token_dependency = Annotated[str, Depends(oauth2_scheme)]
db_dependency = Annotated[Session, Depends(get_db)]


def get_auth_service(db: db_dependency) -> AuthService:
    user_repo = UserRepository(db)
    return AuthService(user_repo)

def get_user_service(db: db_dependency) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]
auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(token: token_dependency, auth_service: auth_service_dependency):
    return auth_service.get_current_user(token)

user_dependency = Annotated[dict, Depends(get_current_user)]