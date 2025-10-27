from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from app.schema.response import StandardResponse, success
from app.schema.shopping import CartItemCreate, ShoppingCartOut, OrderCreate, OrderOut
from app.service.shopping import ShoppingService
from app.api.deps import get_shopping_service
from app.entities.user import User
from app.core.auth import get_current_user  # your existing auth

router = APIRouter(prefix="/shopping", tags=["Shopping"])


@router.post("/cart/items", response_model=StandardResponse[ShoppingCartOut])
async def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    service: ShoppingService = Depends(get_shopping_service)
):
    await service.add_to_cart(current_user.id, item)
    cart = await service.get_cart(current_user.id)
    return success(cart)


@router.get("/cart", response_model=StandardResponse[ShoppingCartOut])
async def view_cart(
    current_user: User = Depends(get_current_user),
    service: ShoppingService = Depends(get_shopping_service)
):
    cart = await service.get_cart(current_user.id)
    return success(cart)


@router.post("/checkout", response_model=StandardResponse[OrderOut])
async def checkout(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    service: ShoppingService = Depends(get_shopping_service)
):
    if not order_data.dataset_ids:
        raise HTTPException(status_code=400, detail="No datasets selected")
    order = await service.checkout(current_user.id, order_data)
    return success(order)


@router.get("/orders", response_model=StandardResponse[Page[OrderOut]])
async def list_orders(
    params: Params = Depends(),
    current_user: User = Depends(get_current_user),
    service: ShoppingService = Depends(get_shopping_service)
):
    # In real app, add pagination to repo
    orders = await service.list_orders(current_user.id)  # implement in service
    return success(orders)
