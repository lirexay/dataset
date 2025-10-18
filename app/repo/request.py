from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from schema.request import RequestCreate, RequestUpdate
from entities.request import Request


class RequestsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, request_id: int) -> Optional[Request]:
        q = await self.db.execute(select(Request).where(Request.id == request_id))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[Request]:
        q = select(Request).order_by(Request.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: RequestCreate) -> Request:
        db_obj = Request(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Request, payload: RequestUpdate) -> Request:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
