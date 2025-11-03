from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from models.models import Users
from dependecies.auth_dependency import get_current_user
from db.database import get_db
from schemas.auth_schemas import PasswordChangeRequest
from services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    return db.query(Users).filter(Users.id == user.id).first()


@router.put("/user/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, request: PasswordChangeRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    user_model = db.query(Users).filter(Users.id == user.id).first()

    authservice = AuthService(db)

    if not authservice.verify_password(request.old_password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid old password"
        )

    user_model.hashed_password = authservice.hash_password(request.new_password)
    db.add(user_model)
    db.commit()
