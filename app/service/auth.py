from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from app.repo.auth import AuthRepo
from app.schema.auth import UserCreate


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepo(db)

    async def get_user(self, username: str, password: str):
        return await self.repo.get(username=username, password=password)

    async def get_user_by_username(self, username: str):
        return await self.repo.get_by_username(username=username)
