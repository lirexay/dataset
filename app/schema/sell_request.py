from pydantic import BaseModel


class SellRequestBase(BaseModel):
    title: str
    description: str
    comment: str
    state_id: int
    user_requestor_id: int


class SellRequestCreate(SellRequestBase):
    pass


class SellRequestUpdate(SellRequestBase):
    pass


class SellRequestOut(SellRequestBase):
    id: int

    class Config:
        from_attributes = True
