
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.models import Users


from typing import Optional

class UserRepository:
    """ Handles all database operations for users"""
    def __init__(self, db:Session):
        self.db = db
    def get_by_id(self, user_id: int) -> Optional[Users]:
        return self.db.query(Users).filter(Users.id == user_id).first()
        
    def get_by_email(self, user_email: str) -> Optional[Users]:
        return self.db.query(Users).filter(Users.email == user_email).first()
    def get_by_username(self, username: str) -> Optional[Users]:
        return self.db.query(Users).filter(Users.username == username).first()

    def create_user(self, user:Users) -> None:
        try:
            self.db.add(user)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("User already exists")
    def update_password(self, user_id: int, new_hashed_password: str) -> None:
        """
        Update user's password in db
        Note: Expects already hashed password
        """
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        user.hashed_password = new_hashed_password
        self.db.commit()
        


