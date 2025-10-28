# schema/dataset_category.py
from pydantic import BaseModel
from typing import Optional


class DatasetCategoryBase(BaseModel):
    name: str


class DatasetCategoryCreate(DatasetCategoryBase):
    pass


class DatasetCategoryUpdate(DatasetCategoryBase):
    pass


class DatasetCategoryOut(DatasetCategoryBase):
    id: int

    class Config:
        from_attributes = True
