from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from schema.sell_request import SellRequestCreate, SellRequestUpdate
from entities.sell_request import SellRequest


class SellRequestsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, sell_request_id: int) -> Optional[SellRequest]:
        q = await self.db.execute(select(SellRequest).where(SellRequest.id == sell_request_id))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[SellRequest]:
        q = select(SellRequest).order_by(SellRequest.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: SellRequestCreate) -> SellRequest:
        db_obj = SellRequest(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: SellRequest, payload: SellRequestUpdate) -> SellRequest:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
