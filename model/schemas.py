from typing import Optional
from pydantic import BaseModel
from datetime import date


# login
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    role_id: int


class TokenData(BaseModel):
    username: str | None = None


# User schemas

class UserChangePassword(BaseModel):
    password: str


class UserCreate(BaseModel):
    fname: str
    lname: str
    username: str
    password: str
    phone: str


class UserUpdateRequest(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    father_name: str
    birth: date
    resume_file_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    active: bool

    class Config:
        from_attributes = True


class UserMeInfoResponse(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class UserInfoResponse(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    father_name: str
    birth: date
    resume_file_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    active: bool
    user_type_id: int

    class Config:
        from_attributes = True


class UserInfoLimitedResponse(BaseModel):
    id: int
    fname: str
    lname: str

    class Config:
        from_attributes = True


# state
class StateResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# requests
class RequestResponse(BaseModel):
    id: int
    title: str
    description: str
    comment: str
    requestor: UserInfoResponse
    state: StateResponse

    class Config:
        from_attributes = True


class RequestUpdate(BaseModel):
    state: int  # ENUM
    comment: str

    class Config:
        from_attributes = True


class RequestAddRequest(BaseModel):
    title: str
    description: str
    comment: str
    state_id: int

    class Config:
        from_attributes = True


# dataset
class DatasetResponse(BaseModel):
    id: int
    name: str
    description: str
    file_id: int

    class Config:
        from_attributes = True


class DatasetLimitedResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
