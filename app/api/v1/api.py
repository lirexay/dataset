from fastapi import APIRouter
from app.core.config import settings
from app.controller.item import router as item_router
from app.controller.dataset import router as dataset_router
from app.controller.file import router as file_router
from app.controller.request import router as request_router
from app.controller.sell_request import router as sell_request_router
from app.controller.user import router as user_router
from app.controller.user_role import router as user_role_router
from app.controller.state import router as state_router
from app.controller.auth import router as auth_router
from app.controller.seed import router as seed_router


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
