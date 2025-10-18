from pydantic import BaseModel


class RequestBase(BaseModel):
    title: str
    description: str
    comment: str
    state_id: int
    user_requestor_id: int


class RequestCreate(RequestBase):
    pass


class RequestUpdate(RequestBase):
    pass


class RequestOut(RequestBase):
    id: int

    class Config:
        from_attributes = True
