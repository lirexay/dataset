from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from app.repo.sell_request import SellRequestsRepo
from app.schema.sell_request import SellRequestCreate, SellRequestUpdate


class SellRequestsService:
    def __init__(self, db: AsyncSession):
        self.repo = SellRequestsRepo(db)

    async def create_sell_request(self, payload: SellRequestCreate):
        return await self.repo.create(payload)

    async def get_sell_request(self, sell_request_id: int):
        return await self.repo.get(sell_request_id)

    async def list_sell_requests(self, params: Params):
        return await self.repo.list(params)

    async def update_sell_request(self, sell_request_id: int, payload: SellRequestUpdate):
        db_obj = await self.repo.get(sell_request_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
