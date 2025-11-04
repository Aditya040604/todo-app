from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated

from schemas.auth_schemas import CreateUserRequest, Token
from dependecies.auth_dependency import user_service_dependency, auth_service_dependency

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_service: user_service_dependency, create_user_request: CreateUserRequest):
    user_service.create_user(create_user_request)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: auth_service_dependency
):
    token = auth_service.authenticate_user(formData.username, formData.password)
    return {"access_token": token, "token_type": "bearer"}
