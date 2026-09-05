from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import ProductInventory


class InventoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, inventory_id: int):
        stmt = (
            select(ProductInventory)
            .where(ProductInventory.id == inventory_id)
        )

        return self.session.scalar(stmt)

    def get_by_product(self, product_id: int):
        stmt = (
            select(ProductInventory)
            .where(ProductInventory.product_id == product_id)
        )

        return self.session.scalar(stmt)

    def get_available_quantity(self, product_id: int):
        inventory = self.get_by_product(product_id)

        if inventory is None:
            return None

        return (
            inventory.stock_quantity
            - inventory.reserved_quantity
        )

    def create(
        self,
        product_id: int,
        stock_quantity: int = 0,
        reserved_quantity: int = 0,
    ):
        inventory = ProductInventory(
            product_id=product_id,
            stock_quantity=stock_quantity,
            reserved_quantity=reserved_quantity,
        )

        self.session.add(inventory)
        self.session.flush()

        return inventory

    def update(
        self,
        inventory: ProductInventory,
        stock_quantity: int | None = None,
        reserved_quantity: int | None = None,
    ):
        if stock_quantity is not None:
            inventory.stock_quantity = stock_quantity

        if reserved_quantity is not None:
            inventory.reserved_quantity = reserved_quantity

        self.session.flush()

        return inventory

    def delete(self, inventory: ProductInventory):
        self.session.delete(inventory)
        self.session.flush()