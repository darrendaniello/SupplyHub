from sqlalchemy.orm import Session

from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository


class OrderService:
    def __init__(self, session: Session):
        self.order_repository = OrderRepository(session)
        self.order_item_repository = OrderItemRepository(session)

    def get_user_orders(self, user_id: int):
        return self.order_repository.get_by_buyer(user_id)

    def get_order_detail(self, user_id: int, order_id: int):
        order = self.order_repository.get_by_id(order_id)

        if order is None:
            raise ValueError("Order not found")

        if order.buyer_id != user_id:
            raise ValueError("Order does not belong to this user")

        items = self.order_item_repository.get_by_order(order_id)

        return {
            "order": order,
            "items": items,
        }