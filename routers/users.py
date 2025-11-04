from fastapi import APIRouter, HTTPException
from starlette import status
from dependecies.auth_dependency import user_dependency, user_service_dependency
from schemas.auth_schemas import PasswordChangeRequest

router = APIRouter(prefix="/users", tags=["users"])




@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, user_service: user_service_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    return user


@router.put("/user/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, user_service: user_service_dependency, request: PasswordChangeRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    user_service.change_password(user.id,request.old_password, request.new_password)

