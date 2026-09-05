from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.order_item import OrderItem

class OrderItemRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_item_id: id):
        stmt = select(OrderItem).where(OrderItem.id == order_item_id)

        return self.session.scalar(stmt)

    def get_by_order(self, order_id: int):
        stmt = (
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
        )

        return self.session.scalars(stmt).all()

    def get_by_product(self, product_id: int):
        stmt = (
            select(OrderItem)
            .where(OrderItem.product_id == product_id)
        )

        return self.session.scalars(stmt).all()

    def create(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price: Decimal,
        subtotal: Decimal,
    ):
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )

        self.session.add(order_item)
        self.session.flush()

        return order_item

    def update(
        self,
        order_item: OrderItem,
        quantity: int | None = None,
        unit_price: Decimal | None = None,
        subtotal: Decimal | None = None,
    ):
        if quantity is not None:
            order_item.quantity = quantity

        if unit_price is not None:
            order_item.unit_price = unit_price

        if subtotal is not None:
            order_item.subtotal = subtotal

        self.session.flush()

        return order_item

    def delete(self, order_item: OrderItem):
        self.session.delete(order_item)
        self.session.flush()