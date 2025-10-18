from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from entities.user import User


class AuthRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, username: str, password: str) -> Optional[User]:
        q = await self.db.execute(select(User).where(
            (User.username == username) & (User.password == password)))
        return q.scalars().first()

    async def get_by_username(self, username: str) -> Optional[User]:
        q = await self.db.execute(select(User).where(
            (User.username == username)))
        return q.scalars().first()
