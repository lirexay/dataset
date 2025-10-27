from app.service.item import ItemsService
from app.service.sell_request import SellRequestsService
from app.service.request import RequestsService
from app.service.state import StatesService
from app.service.dataset import DatasetsService
from app.service.file import FilesService
from app.service.user import UsersService
from app.service.user_role import UserRolesService
from app.service.auth import AuthService
from service.shopping import ShoppingService
from service.item import ItemsService
from service.sell_request import SellRequestsService
from service.request import RequestsService
from service.state import StatesService
from service.dataset import DatasetsService
from service.file import FilesService
from service.user import UsersService
from service.user_role import UserRolesService
from service.auth import AuthService
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


async def get_shopping_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[ShoppingService, None]:
    yield ShoppingService(db)


async def get_items_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[ItemsService, None]:
    yield ItemsService(db)


async def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(db)


async def get_user_roles_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UserRolesService, None]:
    yield UserRolesService(db)


async def get_users_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UsersService, None]:
    yield UsersService(db)


async def get_files_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[FilesService, None]:
    yield FilesService(db)


async def get_datasets_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[DatasetsService, None]:
    yield DatasetsService(db)


async def get_states_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[StatesService, None]:
    yield StatesService(db)


async def get_requests_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[RequestsService, None]:
    yield RequestsService(db)


async def get_sell_requests_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[SellRequestsService, None]:
    yield SellRequestsService(db)
