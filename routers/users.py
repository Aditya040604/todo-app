from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from .auth import get_current_user, bcrypt_context

router = APIRouter(prefix="/users", tags=["users"])


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None or user.get("id") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    print(user_model)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_model = {
        "first name": user_model.first_name,
        "last name": user_model.last_name,
        "email": user_model.email,
        "username": user_model.username,
    }
    return user_model


@router.put("/user/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, request: PasswordChangeRequest
):
    if user is None or user.get("id") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not bcrypt_context.verify(request.old_password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password"
        )
    if request.old_password == request.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New Password must be different",
        )
    hashed_new_password = bcrypt_context.hash(request.new_password)
    db.query(Users).filter(Users.id == user.get("id")).update(
        {"hashed_password": hashed_new_password}
    )
    db.commit()
    return {"message": "Password changed successfully"}
