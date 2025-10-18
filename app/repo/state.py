from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from schema.state import StateCreate, StateUpdate
from entities.state import State


class StatesRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, state_id: int) -> Optional[State]:
        q = await self.db.execute(select(State).where(State.id == state_id))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[State]:
        q = select(State).order_by(State.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: StateCreate) -> State:
        db_obj = State(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: State, payload: StateUpdate) -> State:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
