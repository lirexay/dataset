from typing import Optional
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from schema.user import UserCreate, UserUpdate
from entities.user import User
from sqlalchemy import update


class UsersRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_password(self, user_id: int, hashed_password: str):
        await self.db.execute(
            update(User).where(User.id == user_id).values(
                password=hashed_password)
        )
        await self.db.commit()

    async def get(self, user_id: int) -> Optional[User]:
        q = await self.db.execute(select(User).where(User.id == user_id))
        return q.scalars().first()

    async def get_by_username(self, username: str):
        q = await self.db.execute(select(User).where(User.username == username))
        return q.scalars().first()

    async def list(self, params: Params) -> Page[User]:
        q = select(User).order_by(User.id)
        return await paginate(self.db, q, params)

    async def create(self, payload: UserCreate) -> User:
        db_obj = User(**payload.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: User, payload: UserUpdate) -> User:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
