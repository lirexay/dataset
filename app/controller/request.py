from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from app.api.deps import get_requests_service
from app.schema.response import StandardResponse, success
from app.schema.request import RequestCreate, RequestOut, RequestUpdate
from app.service.request import RequestsService

router = APIRouter()


@router.post("/", response_model=StandardResponse[RequestOut], status_code=status.HTTP_201_CREATED)
async def create_request(
    payload: RequestCreate,
    service: RequestsService = Depends(get_requests_service)
):
    return success(await service.create_request(payload))


@router.get("/", response_model=StandardResponse[Page[RequestOut]])
async def list_requests(
    params: Params = Depends(),
    service: RequestsService = Depends(get_requests_service)
):
    requests = await service.list_requests(params)
    return success(requests)


@router.get("/{request_id}", response_model=StandardResponse[RequestOut])
async def read_request(request_id: int, service: RequestsService = Depends(get_requests_service)):
    obj = await service.get_request(request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Request not found")
    return success(obj)


@router.put("/{request_id}", response_model=StandardResponse[RequestOut])
async def update_request(
    request_id: int,
    payload: RequestUpdate,
    service: RequestsService = Depends(get_requests_service),
):
    obj = await service.update_request(request_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Request not found")
    return success(obj)
