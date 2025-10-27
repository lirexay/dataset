from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repo.shopping import ShoppingRepo
from schema.shopping import CartItemCreate, OrderCreate


class ShoppingService:
    def __init__(self, db: AsyncSession):
        self.repo = ShoppingRepo(db)

    async def get_or_create_cart(self, user_id: int):
        cart = await self.repo.get_active_cart_by_user(user_id)
        if not cart:
            cart = await self.repo.create_cart(user_id)
        return cart

    async def add_to_cart(self, user_id: int, item: CartItemCreate):
        cart = await self.get_or_create_cart(user_id)
        return await self.repo.add_item_to_cart(cart.id, item)

    async def get_cart(self, user_id: int):
        cart = await self.repo.get_active_cart_by_user(user_id)
        if not cart:
            return {"items": []}
        full_cart = await self.repo.get_cart_with_items(cart.id)
        return full_cart

    async def checkout(self, user_id: int, order_data: OrderCreate):
        # Validate datasets exist
        datasets = await self.repo.get_datasets_by_ids(order_data.dataset_ids)
        if len(datasets) != len(order_data.dataset_ids):
            raise HTTPException(
                status_code=404, detail="One or more datasets not found")

        # Calculate total (in real app, use actual price from Dataset model)
        total = float(len(datasets) * 100.0)  # $100 per dataset for demo

        # Create order
        order = await self.repo.create_order(user_id, total)

        # Create order items (store price at time of purchase)
        items = [
            {"dataset_id": d.id, "price_at_purchase": 100.0}
            for d in datasets
        ]
        await self.repo.create_order_items(order.id, items)

        # Clear cart
        cart = await self.repo.get_active_cart_by_user(user_id)
        if cart:
            cart.is_active = False
            await self.db.commit()

        return order
