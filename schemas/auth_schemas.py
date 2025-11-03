from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

class Payload(BaseModel):
    user_name: str
    user_id: int
    user_role: str