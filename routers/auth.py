from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from datetime import timedelta

from db.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

from schemas.auth_schemas import CreateUserRequest, Token, Payload
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    auth_service = AuthService(db)
    auth_service.create_user(create_user_request)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(formData.username, formData.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    data = Payload(user_name=user.username, user_id=user.id, user_role=user.role)
    token = auth_service.create_access_token(data  ,timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}
