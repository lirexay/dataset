import asyncio
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager

from api.v1.api import router as api_v1_router
from core.config import settings
from core.logging import configure_logging
from utils.error import register_error_handlers

# 👇 Import ALL entity models so Base.metadata includes them
from entities.user_role import UserRole
from entities.user import User
from entities.file import File
from entities.dataset import Dataset
from entities.state import State
from entities.request import Request
from entities.sell_request import SellRequest
from entities.item import Item

# Database setup
from db.base import Base
from db.session import engine


configure_logging()


async def create_tables():
    """Create all tables defined in Base.metadata."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    await create_tables()
    yield
    # Shutdown: nothing to do here for now


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan  # ← Use lifespan to manage startup/shutdown
    )
    add_pagination(app)

    register_error_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix="/api/v1")

    @app.get("/ping")
    async def ping():
        return "pong"

    @app.get("/error")
    async def error():
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return app


app = create_app()
