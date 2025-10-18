from pydantic import BaseModel


class UserRoleBase(BaseModel):
    title: str


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(UserRoleBase):
    pass


class UserRoleOut(UserRoleBase):
    id: int

    class Config:
        from_attributes = True
