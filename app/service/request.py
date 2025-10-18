
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from repo.request import RequestsRepo
from schema.request import RequestCreate, RequestUpdate


class RequestsService:
    def __init__(self, db: AsyncSession):
        self.repo = RequestsRepo(db)

    async def create_request(self, payload: RequestCreate):
        return await self.repo.create(payload)

    async def get_request(self, request_id: int):
        return await self.repo.get(request_id)

    async def list_requests(self, params: Params):
        return await self.repo.list(params)

    async def update_request(self, request_id: int, payload: RequestUpdate):
        db_obj = await self.repo.get(request_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
