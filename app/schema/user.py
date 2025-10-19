from pydantic import BaseModel


class UserBase(BaseModel):
    user_role_id: int
    fname: str
    lname: str
    username: str
    password: str  # ⚠️ Should be write-only; consider excluding from response
    phone: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    user_role_id: int
    fname: str
    lname: str
    username: str
    phone: str

    class Config:
        from_attributes = True
