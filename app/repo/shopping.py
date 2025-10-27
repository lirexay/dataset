from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.shopping_cart import ShoppingCart
from app.entities.cart_item import CartItem
from app.entities.order import Order
from app.entities.order_item import OrderItem
from app.entities.dataset import Dataset
from app.schema.shopping import CartItemCreate


class ShoppingRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active_cart_by_user(self, user_id: int) -> Optional[ShoppingCart]:
        q = await self.db.execute(
            select(ShoppingCart).where(
                and_(ShoppingCart.user_id == user_id,
                     ShoppingCart.is_active == True)
            )
        )
        return q.scalars().first()

    async def create_cart(self, user_id: int) -> ShoppingCart:
        cart = ShoppingCart(user_id=user_id)
        self.db.add(cart)
        await self.db.flush()
        return cart

    async def add_item_to_cart(self, cart_id: int, item: CartItemCreate) -> CartItem:
        cart_item = CartItem(cart_id=cart_id, dataset_id=item.dataset_id)
        self.db.add(cart_item)
        await self.db.flush()
        return cart_item

    async def get_cart_with_items(self, cart_id: int):
        q = await self.db.execute(
            select(ShoppingCart)
            .where(ShoppingCart.id == cart_id)
            .join(CartItem, isouter=True)
        )
        return q.scalars().first()

    async def get_datasets_by_ids(self, dataset_ids: List[int]):
        q = await self.db.execute(select(Dataset).where(Dataset.id.in_(dataset_ids)))
        return q.scalars().all()

    async def create_order(self, user_id: int, total: float) -> Order:
        order = Order(user_id=user_id, total_amount=total)
        self.db.add(order)
        await self.db.flush()
        return order

    async def create_order_items(self, order_id: int, items: List[dict]):
        order_items = [OrderItem(order_id=order_id, **item) for item in items]
        self.db.add_all(order_items)
        await self.db.flush()
