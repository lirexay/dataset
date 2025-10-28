# service/dataset_category.py
from fastapi import HTTPException, status
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from app.repo.dataset_category import DatasetCategoriesRepo
from app.schema.dataset_category import DatasetCategoryCreate, DatasetCategoryUpdate


class DatasetCategoriesService:
    def __init__(self, db: AsyncSession):
        self.repo = DatasetCategoriesRepo(db)

    async def create_category(self, payload: DatasetCategoryCreate):
        existing = await self.repo.get_by_name(payload.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists"
            )
        return await self.repo.create(payload)

    async def get_category(self, category_id: int):
        return await self.repo.get(category_id)

    async def list_categories(self, params: Params):
        return await self.repo.list(params)

    async def update_category(self, category_id: int, payload: DatasetCategoryUpdate):
        db_obj = await self.repo.get(category_id)
        if not db_obj:
            return None
        # Check for name conflict (excluding self)
        if payload.name != db_obj.name:
            existing = await self.repo.get_by_name(payload.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category name already taken"
                )
        return await self.repo.update(db_obj, payload)

    async def delete_category(self, category_id: int):
        db_obj = await self.repo.get(category_id)
        if not db_obj:
            return False
        await self.repo.delete(db_obj)
        return True
