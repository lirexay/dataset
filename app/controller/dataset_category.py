# controller/dataset_category.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from app.schema.response import StandardResponse, success
from app.schema.dataset_category import DatasetCategoryCreate, DatasetCategoryOut, DatasetCategoryUpdate
from app.service.dataset_category import DatasetCategoriesService
from app.api.deps import get_dataset_categories_service

router = APIRouter(prefix="/categories", tags=["Dataset Categories"])


@router.post(
    "/",
    response_model=StandardResponse[DatasetCategoryOut],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new dataset category"
)
async def create_category(
    payload: DatasetCategoryCreate,
    service: DatasetCategoriesService = Depends(get_dataset_categories_service)
):
    return success(await service.create_category(payload))


@router.get(
    "/",
    response_model=StandardResponse[Page[DatasetCategoryOut]],
    summary="List all dataset categories"
)
async def list_categories(
    params: Params = Depends(),
    service: DatasetCategoriesService = Depends(get_dataset_categories_service)
):
    categories = await service.list_categories(params)
    return success(categories)


@router.get(
    "/{category_id}",
    response_model=StandardResponse[DatasetCategoryOut],
    summary="Get a dataset category by ID"
)
async def read_category(
    category_id: int,
    service: DatasetCategoriesService = Depends(get_dataset_categories_service)
):
    obj = await service.get_category(category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return success(obj)


@router.put(
    "/{category_id}",
    response_model=StandardResponse[DatasetCategoryOut],
    summary="Update a dataset category"
)
async def update_category(
    category_id: int,
    payload: DatasetCategoryUpdate,
    service: DatasetCategoriesService = Depends(
        get_dataset_categories_service),
):
    obj = await service.update_category(category_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return success(obj)


@router.delete(
    "/{category_id}",
    response_model=StandardResponse[bool],
    summary="Delete a dataset category"
)
async def delete_category(
    category_id: int,
    service: DatasetCategoriesService = Depends(
        get_dataset_categories_service),
):
    success_delete = await service.delete_category(category_id)
    if not success_delete:
        raise HTTPException(status_code=404, detail="Category not found")
    return success(True)
