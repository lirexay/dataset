from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from api.deps import get_sell_requests_service
from schema.response import StandardResponse, success
from schema.sell_request import SellRequestCreate, SellRequestOut, SellRequestUpdate
from service.sell_request import SellRequestsService

router = APIRouter()


@router.post("/", response_model=StandardResponse[SellRequestOut], status_code=status.HTTP_201_CREATED)
async def create_sell_request(
    payload: SellRequestCreate,
    service: SellRequestsService = Depends(get_sell_requests_service)
):
    return success(await service.create_sell_request(payload))


@router.get("/", response_model=StandardResponse[Page[SellRequestOut]])
async def list_sell_requests(
    params: Params = Depends(),
    service: SellRequestsService = Depends(get_sell_requests_service)
):
    sell_requests = await service.list_sell_requests(params)
    return success(sell_requests)


@router.get("/{sell_request_id}", response_model=StandardResponse[SellRequestOut])
async def read_sell_request(sell_request_id: int, service: SellRequestsService = Depends(get_sell_requests_service)):
    obj = await service.get_sell_request(sell_request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sell request not found")
    return success(obj)


@router.put("/{sell_request_id}", response_model=StandardResponse[SellRequestOut])
async def update_sell_request(
    sell_request_id: int,
    payload: SellRequestUpdate,
    service: SellRequestsService = Depends(get_sell_requests_service),
):
    obj = await service.update_sell_request(sell_request_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Sell request not found")
    return success(obj)
