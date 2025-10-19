from datetime import date
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, Field


class UserInfoResponse(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    birth: date

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    fname: str
    lname: str
    username: str
    password: str = Field(..., min_length=6)
    phone: str
    user_role_id: int = 4  # Default: "مشتری" (Customer)


class UserOut(BaseModel):
    id: int
    fname: str
    lname: str
    username: str
    phone: str
    user_role_id: int

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    username: str  # or email, if you add email field later


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
