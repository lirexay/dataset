from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from app.repo.user_role import UserRolesRepo
from app.schema.user_role import UserRoleCreate, UserRoleUpdate


class UserRolesService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRolesRepo(db)

    async def create_user_role(self, payload: UserRoleCreate):
        return await self.repo.create(payload)

    async def get_user_role(self, role_id: int):
        return await self.repo.get(role_id)

    async def list_user_roles(self, params: Params):
        return await self.repo.list(params)

    async def update_user_role(self, role_id: int, payload: UserRoleUpdate):
        db_obj = await self.repo.get(role_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
