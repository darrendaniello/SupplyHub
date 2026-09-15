from decimal import Decimal
from sqlalchemy.orm import Session

from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.cart_repository import CartRepository


class OrderService:
    def __init__(self, session: Session):
        self.order_repository = OrderRepository(session)
        self.order_item_repository = OrderItemRepository(session)
        self.cart_repository = CartRepository(session)

    def get_user_orders(self, user_id: int):
        return self.order_repository.get_by_buyer(user_id)

    def get_order_detail(self, user_id: int, order_id: int):
        order = self.order_repository.get_by_id(order_id)

        if order is None:
            raise ValueError("Order not found")

        print("DETAIL USER ID:", user_id)
        print("ORDER BUYER ID:", order.buyer_id)
        print("ORDER ID:", order.id)

        if order.buyer_id != user_id:
            raise ValueError("Order does not belong to this user")

        items = self.order_item_repository.get_by_order(order_id)

        return {
            "order": order,
            "items": items,
        }

    def create_order(
        self,
        user_id: int,
        shipping_address: str,
    ):
        if not shipping_address or not shipping_address.strip():
            raise ValueError("Shipping address is required")

        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            raise ValueError("Cart not found")

        cart_items = self.cart_repository.get_items_by_cart(cart.id)

        if not cart_items:
            raise ValueError("Cart is empty")

        supplier_business_id = None
        total_amount = Decimal("0")
        order_items_data = []

        for cart_item in cart_items:
            product = cart_item.product

            if product is None:
                raise ValueError("Product not found")

            if cart_item.quantity <= 0:
                raise ValueError(
                    f"Invalid quantity for product: {product.name}"
                )

            if product.inventory is None:
                raise ValueError(
                    f"Inventory not found for product: {product.name}"
                )

            if (
                product.inventory.stock_quantity
                - product.inventory.reserved_quantity
                < cart_item.quantity
            ):
                raise ValueError(
                    f"Insufficient stock for product: {product.name}"
                )

            current_supplier_id = product.business_id

            if supplier_business_id is None:
                supplier_business_id = current_supplier_id
            elif supplier_business_id != current_supplier_id:
                raise ValueError(
                    "Checkout can only contain products from one supplier"
                )

            price = Decimal(str(product.selling_price))
            subtotal = price * cart_item.quantity
            total_amount += subtotal

            order_items_data.append(
                {
                    "product": product,
                    "product_id": product.id,
                    "quantity": cart_item.quantity,
                    "price": price,
                    "subtotal": subtotal,
                }
            )

        if supplier_business_id is None:
            raise ValueError("Supplier business not found")

        order = self.order_repository.create(
            buyer_id=int(user_id),
            supplier_business_id=supplier_business_id,
            shipping_address=shipping_address,
            total_amount=total_amount,
        )

        for item_data in order_items_data:
            self.order_item_repository.create(
                order_id=order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["price"],
                subtotal=item_data["subtotal"],
            )

            product = item_data["product"]
            product.inventory.stock_quantity -= item_data["quantity"]

        for cart_item in cart_items:
            self.cart_repository.delete_item(cart_item)

        return order