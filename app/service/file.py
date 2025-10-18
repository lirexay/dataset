from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from repo.file import FilesRepo
from schema.file import FileCreate, FileUpdate


class FilesService:
    def __init__(self, db: AsyncSession):
        self.repo = FilesRepo(db)

    async def create_file(self, payload: FileCreate):
        return await self.repo.create(payload)

    async def get_file(self, file_id: int):
        return await self.repo.get(file_id)

    async def list_files(self, params: Params):
        return await self.repo.list(params)

    async def update_file(self, file_id: int, payload: FileUpdate):
        db_obj = await self.repo.get(file_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
