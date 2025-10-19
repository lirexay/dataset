from typing import Optional
from pydantic import BaseModel


class DatasetBase(BaseModel):
    name: str
    description: str
    file_id: int


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(DatasetBase):
    pass


class DatasetOut(DatasetBase):
    id: int

    class Config:
        from_attributes = True


class DatasetFilter(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file_id: Optional[int] = None
