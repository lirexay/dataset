from fastapi_pagination import Params
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from entities.user import User
from repo.user import UsersRepo
from schema.user import UserCreate, UserUpdate
from core.auth import (
    create_access_token,
    create_password_reset_token,
    get_current_user,
    get_password_hash,
    verify_password,
)


class UsersService:
    def __init__(self, db: AsyncSession):
        self.repo = UsersRepo(db)

    async def initiate_password_reset(self, username: str) -> str:
        """Returns reset token (in real app, send via email)"""
        user = await self.repo.get_by_username(username)
        if not user:
            # Don't reveal if user exists (security best practice)
            return None
        return create_password_reset_token(username)

    async def reset_password(self, token: str, new_password: str) -> bool:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            if payload.get("type") != "password_reset":
                return False
            username: str = payload.get("sub")
            if username is None:
                return False
        except JWTError:
            return False

        user = await self.repo.get_by_username(username)
        if not user:
            return False

        hashed_pw = get_password_hash(new_password)
        await self.repo.update_password(user.id, hashed_pw)
        return True

    async def create_user(self, payload: UserCreate) -> User:
        # Check if username already exists
        existing = await self.repo.get_by_username(payload.username)
        if existing:
            raise ValueError("Username already taken")

        # Hash password
        hashed_pw = get_password_hash(payload.password)

        # Create user
        user_data = payload.model_dump(exclude={"password"})
        user_data["password"] = hashed_pw
        return await self.repo.create(user_data)

    async def create_user(self, payload: UserCreate):
        return await self.repo.create(payload)

    async def get_user(self, user_id: int):
        return await self.repo.get(user_id)

    async def list_users(self, params: Params):
        return await self.repo.list(params)

    async def update_user(self, user_id: int, payload: UserUpdate):
        db_obj = await self.repo.get(user_id)
        if not db_obj:
            return None
        return await self.repo.update(db_obj, payload)
