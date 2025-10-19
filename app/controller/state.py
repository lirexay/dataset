from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from app.api.deps import get_states_service
from app.schema.response import StandardResponse, success
from app.schema.state import StateCreate, StateOut, StateUpdate
from app.service.state import StatesService

router = APIRouter()


@router.post("/", response_model=StandardResponse[StateOut], status_code=status.HTTP_201_CREATED)
async def create_state(
    payload: StateCreate,
    service: StatesService = Depends(get_states_service)
):
    return success(await service.create_state(payload))


@router.get("/", response_model=StandardResponse[Page[StateOut]])
async def list_states(
    params: Params = Depends(),
    service: StatesService = Depends(get_states_service)
):
    states = await service.list_states(params)
    return success(states)


@router.get("/{state_id}", response_model=StandardResponse[StateOut])
async def read_state(state_id: int, service: StatesService = Depends(get_states_service)):
    obj = await service.get_state(state_id)
    if not obj:
        raise HTTPException(status_code=404, detail="State not found")
    return success(obj)


@router.put("/{state_id}", response_model=StandardResponse[StateOut])
async def update_state(
    state_id: int,
    payload: StateUpdate,
    service: StatesService = Depends(get_states_service),
):
    obj = await service.update_state(state_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="State not found")
    return success(obj)
