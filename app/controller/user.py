from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from api.deps import get_users_service
from schema.response import StandardResponse, success
from schema.user import UserCreate, UserOut, UserUpdate
from service.user import UsersService

router = APIRouter()


@router.post("/", response_model=StandardResponse[UserOut], status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UsersService = Depends(get_users_service)
):
    return success(await service.create_user(payload))


@router.get("/", response_model=StandardResponse[Page[UserOut]])
async def list_users(
    params: Params = Depends(),
    service: UsersService = Depends(get_users_service)
):
    users = await service.list_users(params)
    return success(users)


@router.get("/{user_id}", response_model=StandardResponse[UserOut])
async def read_user(user_id: int, service: UsersService = Depends(get_users_service)):
    obj = await service.get_user(user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return success(obj)


@router.put("/{user_id}", response_model=StandardResponse[UserOut])
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UsersService = Depends(get_users_service),
):
    obj = await service.update_user(user_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return success(obj)
