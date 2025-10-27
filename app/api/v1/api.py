from fastapi import APIRouter
from core.config import settings
from controller.item import router as item_router
from controller.dataset import router as dataset_router
from controller.file import router as file_router
from controller.request import router as request_router
from controller.sell_request import router as sell_request_router
from controller.user import router as user_router
from controller.user_role import router as user_role_router
from controller.state import router as state_router
from controller.auth import router as auth_router
from controller.seed import router as seed_router
from controller.shopping import router as shopping_router

router = APIRouter()


if settings.SEED_ENABLED:
    pass
router.include_router(seed_router, prefix="/dev", tags=["Development"])
router.include_router(state_router, prefix="/state", tags=["state"])
router.include_router(dataset_router, prefix="/dataset", tags=["dataset"])
router.include_router(file_router, prefix="/file", tags=["file"])
router.include_router(request_router, prefix="/request", tags=["request"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(user_router, prefix="/shoping", tags=["shoping"])

router.include_router(
    sell_request_router, prefix="/sell_request", tags=["sell_request"]
)
router.include_router(
    user_role_router, prefix="/user_role", tags=["user_role"]
)
