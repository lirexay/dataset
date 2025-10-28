# repo/dataset_category.py
from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from entities.dataset_category import DatasetCategory
from schema.dataset_category import DatasetCategoryCreate, DatasetCategoryUpdate


class DatasetCategoriesRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, category_id: int) -> Optional[DatasetCategory]:
        q = await self.db.execute(select(DatasetCategory).where(DatasetCategory.id == category_id))
        return q.scalars().first()

    async def get_by_name(self, name: str) -> Optional[DatasetCategory]:
        q = await self.db.execute(select(DatasetCategory).where(DatasetCategory.name == name))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[DatasetCategory]:
        q = select(DatasetCategory).order_by(DatasetCategory.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: DatasetCategoryCreate) -> DatasetCategory:
        db_obj = DatasetCategory(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: DatasetCategory, payload: DatasetCategoryUpdate) -> DatasetCategory:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: DatasetCategory) -> None:
        await self.db.delete(db_obj)
        await self.db.commit()
