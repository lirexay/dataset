from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from app.schema.user_role import UserRoleCreate, UserRoleUpdate
from app.entities.user_role import UserRole


class UserRolesRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, role_id: int) -> Optional[UserRole]:
        q = await self.db.execute(select(UserRole).where(UserRole.id == role_id))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[UserRole]:
        q = select(UserRole).order_by(UserRole.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: UserRoleCreate) -> UserRole:
        db_obj = UserRole(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: UserRole, payload: UserRoleUpdate) -> UserRole:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
