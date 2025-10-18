from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from api.deps import get_datasets_service
from schema.response import StandardResponse, success
from schema.dataset import DatasetCreate, DatasetOut, DatasetUpdate
from service.dataset import DatasetsService

router = APIRouter()


@router.post("/", response_model=StandardResponse[DatasetOut], status_code=status.HTTP_201_CREATED)
async def create_dataset(
    payload: DatasetCreate,
    service: DatasetsService = Depends(get_datasets_service)
):
    return success(await service.create_dataset(payload))


@router.get("/", response_model=StandardResponse[Page[DatasetOut]])
async def list_datasets(
    params: Params = Depends(),
    service: DatasetsService = Depends(get_datasets_service)
):
    datasets = await service.list_datasets(params)
    return success(datasets)


@router.get("/{dataset_id}", response_model=StandardResponse[DatasetOut])
async def read_dataset(dataset_id: int, service: DatasetsService = Depends(get_datasets_service)):
    obj = await service.get_dataset(dataset_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return success(obj)


@router.put("/{dataset_id}", response_model=StandardResponse[DatasetOut])
async def update_dataset(
    dataset_id: int,
    payload: DatasetUpdate,
    service: DatasetsService = Depends(get_datasets_service),
):
    obj = await service.update_dataset(dataset_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return success(obj)
