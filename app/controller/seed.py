# controller/seed.py
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.service.seed import SeedService
from app.core.config import settings
from app.schema.response import StandardResponse, success

from app.db.base import Base
from app.db.session import engine
router = APIRouter()


@router.post(
    "/seed/",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_201_CREATED,
    summary="Seed database with Persian sample data"
)
async def seed_database(db: AsyncSession = Depends(get_db)):

    if not settings.SEED_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seeding is disabled in this environment"
        )
    seed_service = SeedService(db)
    result = await seed_service.seed_all()
    return success(result)
