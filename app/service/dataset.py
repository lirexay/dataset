from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from repo.dataset import DatasetsRepo
from schema.dataset import DatasetCreate, DatasetUpdate


class DatasetsService:
    def __init__(self, db: AsyncSession):
        self.repo = DatasetsRepo(db)

    async def create_dataset(self, payload: DatasetCreate):
        return await self.repo.create(payload)

    async def get_dataset(self, dataset_id: int):
        return await self.repo.get(dataset_id)

    async def list_datasets(self, params: Params):
        return await self.repo.list(params)

    async def update_dataset(self, dataset_id: int, payload: DatasetUpdate):
        db_obj = await self.repo.get(dataset_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
