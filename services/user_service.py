from fastapi import HTTPException
from starlette import status

from repositories.user_repo import UserRepository
from schemas.auth_schemas import CreateUserRequest
from core.security import hash_password, verify_password
from core.security import hash_password
from models.models import Users


class UserService:
    """
    Handles all user crud operations
    """
    def __init__(self, repo:UserRepository):
        self.repo = repo

    def create_user(self, user_data:CreateUserRequest):
        """
        check if user already exists 
        if not create 
        """
        existing_user = self.repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        hashed_password = hash_password(user_data.password)
        user_model = Users(username= user_data.username, email=user_data.email, first_name=user_data.first_name, last_name=user_data.last_name, hashed_password=hashed_password,role=user_data.role )
        self.repo.create_user(user_model)
    
    def get_user(self, user_id: int) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    

    def change_password(self, user_id: int, old_password: str, new_password: str) -> None:
        """
        Change user password with business rules:
        1. User must exist
        2. Old password must be correct
        3. New password must meet requirements
        4. New password can't be same as old
        5. Hash the new password
        """
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        if verify_password(new_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different from old password")
        new_hashed_password = hash_password(new_password)
        self.repo.update_password(user_id, new_hashed_password)
        