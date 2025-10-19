from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from app.repo.state import StatesRepo
from app.schema.state import StateCreate, StateUpdate


class StatesService:
    def __init__(self, db: AsyncSession):
        self.repo = StatesRepo(db)

    async def create_state(self, payload: StateCreate):
        return await self.repo.create(payload)

    async def get_state(self, state_id: int):
        return await self.repo.get(state_id)

    async def list_states(self, params: Params):
        return await self.repo.list(params)

    async def update_state(self, state_id: int, payload: StateUpdate):
        db_obj = await self.repo.get(state_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
