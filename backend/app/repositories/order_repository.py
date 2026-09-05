from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models import Order

class OrderRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: int):
        stmt = select(Order).where(Order.id == order_id)

        return self.session.scalar(stmt)

    def get_by_buyer(self, buyer_id: int):
        stmt = select(Order).where(Order.buyer_id == buyer_id).order_by(Order.created_at.desc())

        return self.session.scalars(stmt).all()

    def create(
            self,
            buyer_id: int,
            supplier_business_id: int,
            total_amount: Decimal,
            status: str = "PENDING"
    ):
        order = Order(
            buyer_id = buyer_id,
            supplier_business_id = supplier_business_id,
            total_amount = total_amount,
            status = status,
        )

        self.session.add(order)
        self.session.flush()

        return order

    def update(
            self,
            order: Order,
            status: str | None = None,
            total_amount: Decimal | None = None,
    ):
        if status is not None:
            order.status = status

        if total_amount is not None:
            order.total_amount = total_amount

        self.session.flush()

        return order

    def delete(self, order: Order):
        self.session.delete(order)
        self.session.flush()