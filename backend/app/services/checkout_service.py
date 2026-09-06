from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository

class CheckoutService:
    def __init__(self, session: Session):
        self.cart_repository = CartRepository(session)
        self.inventory_repository = InventoryRepository(session)
        self.order_repository = OrderRepository(session)
        self.order_item_repository = OrderItemRepository(session)

    def checkout(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            raise ValueError("Cart not found.")

        items = self.cart_repository.get_items_by_cart(cart.id)

        if not items:
            raise ValueError("Cart is empty.")

        grouped_items = {}

        for cart_item in items:
            product = cart_item.product

            if product is None:
                raise ValueError("Product not found")

            business_id = product.business_id

            if business_id not in grouped_items:
                grouped_items[business_id] = []

            grouped_items[business_id].append(cart_item)

        for cart_item in items:
            inventory = self.inventory_repository.get_by_product(cart_item.product_id)

            if inventory is None:
                raise ValueError(
                    f"Inventory not found for product {cart_item.product_id}"
                )

            available_quantity = (
                inventory.stock_quantity - inventory.reserved_quantity
            )

            if cart_item.quantity > available_quantity:
                raise ValueError(
                    f"Insufficient stock for product {cart_item.product_id}"
                )

        created_orders = []
        grand_total = Decimal("0.00")

        for business_id, business_items in grouped_items.items():
            order_total = Decimal("0.00")

            for cart_item in business_items:
                product = cart_item.product

                unit_price = product.selling_price
                subtotal = unit_price * cart_item.quantity

                order_total += subtotal

            order = self.order_repository.create(
                buyer_id=user_id,
                supplier_business_id=business_id,
                total_amount=order_total,
                status="PENDING"
            )

            for cart_item in business_items:
                product = cart_item.product

                unit_price = product.selling_price
                subtotal = unit_price * cart_item.quantity

                self.order_item_repository.create(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )

                inventory = self.inventory_repository.get_by_product(
                    cart_item.product_id
                )

                inventory.stock_quantity -= cart_item.quantity

                self.inventory_repository.update(
                    inventory,
                    stock_quantity=inventory.stock_quantity
                )

                created_orders.append(order)
                grand_total += order_total

            for cart_item in items:
                self.cart_repository.delete_item(cart_item)

            return {
                "orders": created_orders,
                "total_amount": grand_total,
            }