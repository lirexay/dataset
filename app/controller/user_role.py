from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params, paginate
from app.api.deps import get_user_roles_service
from app.schema.response import StandardResponse, success
from app.schema.user_role import UserRoleCreate, UserRoleOut, UserRoleUpdate
from app.service.user_role import UserRolesService

router = APIRouter()


@router.post("/", response_model=StandardResponse[UserRoleOut], status_code=status.HTTP_201_CREATED)
async def create_user_role(
    payload: UserRoleCreate,
    service: UserRolesService = Depends(get_user_roles_service)
):
    return success(await service.create_user_role(payload))


@router.get("/", response_model=StandardResponse[Page[UserRoleOut]])
async def list_user_roles(
    params: Params = Depends(),
    service: UserRolesService = Depends(get_user_roles_service)
):
    roles = await service.list_user_roles(params)
    return success(roles)


@router.get("/{role_id}", response_model=StandardResponse[UserRoleOut])
async def read_user_role(role_id: int, service: UserRolesService = Depends(get_user_roles_service)):
    obj = await service.get_user_role(role_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User role not found")
    return success(obj)


@router.put("/{role_id}", response_model=StandardResponse[UserRoleOut])
async def update_user_role(
    role_id: int,
    payload: UserRoleUpdate,
    service: UserRolesService = Depends(get_user_roles_service),
):
    obj = await service.update_user_role(role_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="User role not found")
    return success(obj)
