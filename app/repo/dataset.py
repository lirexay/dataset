from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi_pagination.ext.sqlalchemy import paginate
from schema.dataset import DatasetCreate, DatasetUpdate
from entities.dataset import Dataset
from schema.dataset import DatasetFilter


class DatasetsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def filter(
        self,
        filters: DatasetFilter,
        params: Params,  # for pagination
    ) -> Page[Dataset]:
        query = select(Dataset)

        # Apply filters dynamically
        conditions = []
        if filters.name is not None:
            conditions.append(Dataset.name.ilike(
                f"%{filters.name}%"))  # case-insensitive
        if filters.description is not None:
            conditions.append(Dataset.description.ilike(
                f"%{filters.description}%"))
        if filters.file_id is not None:
            conditions.append(Dataset.file_id == filters.file_id)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(Dataset.id)
        return await paginate(self.db, query, params)

    async def get(self, dataset_id: int) -> Optional[Dataset]:
        q = await self.db.execute(select(Dataset).where(Dataset.id == dataset_id))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[Dataset]:
        q = select(Dataset).order_by(Dataset.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: DatasetCreate) -> Dataset:
        db_obj = Dataset(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Dataset, payload: DatasetUpdate) -> Dataset:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
