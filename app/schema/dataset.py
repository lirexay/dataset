from pydantic import BaseModel
from typing import Optional


class DatasetCategoryBase(BaseModel):
    name: str


class DatasetCategoryCreate(DatasetCategoryBase):
    pass


class DatasetCategoryOut(DatasetCategoryBase):
    id: int

    class Config:
        from_attributes = True


class DatasetBase(BaseModel):
    name: str
    description: str
    file_id: int
    category_id: int  # ← new


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(DatasetBase):
    pass


class DatasetOut(DatasetBase):
    id: int

    class Config:
        from_attributes = True

# Update filter to include category


class DatasetFilter(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file_id: Optional[int] = None
    category_id: Optional[int] = None  # ← new
