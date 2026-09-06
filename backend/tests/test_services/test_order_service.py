from app.database import SessionLocal
from app.services.order_service import OrderService


def test_get_user_orders():
    with SessionLocal() as session:
        service = OrderService(session)

        orders = service.get_user_orders(user_id=1)

        print("User Orders:")

        for order in orders:
            print(
                f"Order ID: {order.id}, "
                f"Supplier Business ID: {order.supplier_business_id}, "
                f"Total: {order.total_amount}, "
                f"Status: {order.status}"
            )


def test_get_order_detail():
    with SessionLocal() as session:
        service = OrderService(session)

        orders = service.get_user_orders(user_id=1)

        if not orders:
            raise ValueError("No orders found for user 1")

        order_id = orders[0].id

        result = service.get_order_detail(
            user_id=1,
            order_id=order_id,
        )

        order = result["order"]
        items = result["items"]

        print("\nOrder Detail:")
        print("Order ID:", order.id)
        print("Supplier Business ID:", order.supplier_business_id)
        print("Total Amount:", order.total_amount)
        print("Status:", order.status)

        print("\nOrder Items:")

        for item in items:
            print(
                f"Product ID: {item.product_id}, "
                f"Quantity: {item.quantity}, "
                f"Unit Price: {item.unit_price}, "
                f"Subtotal: {item.subtotal}"
            )


if __name__ == "__main__":
    test_get_user_orders()
    test_get_order_detail()