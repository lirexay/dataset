from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartItemBase(BaseModel):
    dataset_id: int


class CartItemCreate(CartItemBase):
    pass


class CartItemOut(CartItemBase):
    id: int
    cart_id: int
    added_at: datetime

    class Config:
        from_attributes = True


class ShoppingCartOut(BaseModel):
    id: int
    user_id: int
    is_active: bool
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    dataset_id: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    dataset_ids: List[int]  # datasets to buy


class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    is_paid: bool
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
