from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from .auth import get_current_user
from passlib.context import CryptContext

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
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/user/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, request: PasswordChangeRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(request.old_password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid old password"
        )

    user_model.hashed_password = bcrypt_context.hash(request.new_password)
    db.add(user_model)
    db.commit()
