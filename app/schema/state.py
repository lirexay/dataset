from pydantic import BaseModel


class StateBase(BaseModel):
    name: str


class StateCreate(StateBase):
    pass


class StateUpdate(StateBase):
    pass


class StateOut(StateBase):
    id: int

    class Config:
        from_attributes = True
