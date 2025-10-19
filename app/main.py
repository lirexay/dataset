import asyncio
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager

from app.api.v1.api import router as api_v1_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.utils.error import register_error_handlers

# 👇 Import ALL entity models so Base.metadata includes them
from app.entities.user_role import UserRole
from app.entities.user import User
from app.entities.file import File
from app.entities.dataset import Dataset
from app.entities.state import State
from app.entities.request import Request
from app.entities.sell_request import SellRequest
from app.entities.item import Item

# Database setup
from app.db.base import Base
from app.db.session import engine


configure_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
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
