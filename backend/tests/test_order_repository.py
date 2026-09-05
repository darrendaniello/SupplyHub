from app.database import SessionLocal
from app.repositories.order_repository import OrderRepository
from decimal import Decimal

def test_get_order_by_id():
    with SessionLocal() as session:
        repository = OrderRepository(session)

        order = repository.get_by_id(1)

        if order:
            print("\nOrder found.")
            print(f"ID: {order.id}")
            print(f"Buyer ID: {order.buyer_id}")
            print(f"Supplier Business ID: {order.supplier_business_id}")
            print(f"Status: {order.status}")
        else:
            print("\nOrder not found.")

def test_get_orders_by_buyer():
    with SessionLocal() as session:
        repo = OrderRepository(session)

        orders = repo.get_by_buyer(buyer_id = 1)

        print("\nOrders found:", len(orders))

        for order in orders:
            print(
                f"Order ID: {order.id}, "
                f"Status: {order.status}, "
                f"Created: {order.created_at}"
            )

def test_create_order():
    with SessionLocal() as session:
        repo = OrderRepository(session)

        order = repo.create(
            buyer_id=1,
            supplier_business_id=1,
            total_amount=Decimal("150000.00")
        )

        session.commit()

        print("\nOrder created successfully!")
        print("Order ID:", order.id)
        print("Buyer ID:", order.buyer_id)
        print("Supplier Business ID:", order.supplier_business_id)
        print("Status:", order.status)
        print("Total Amount:", order.total_amount)

def test_update_order():
    with SessionLocal() as session:
        repo = OrderRepository(session)

        order = repo.get_by_id(1)

        if order is None:
            print("\nOrder not found.")
            return

        print("\nBefore update:")
        print("Order ID:", order.id)
        print("Status:", order.status)
        print("Total Amount:", order.total_amount)

        updated_order = repo.update(
            order = order,
            status="PROCESSING",
        )

        session.commit()

        print("\nAfter update:")
        print("Order ID:", updated_order.id)
        print("Status:", updated_order.status)
        print("Total Amount:", updated_order.total_amount)

def test_delete_order():
    with SessionLocal() as session:
        repo = OrderRepository(session)

        order = repo.get_by_id(5)

        if order is None:
            print("\nOrder not found.")
            return

        print("\nBefore delete:")
        print("Order ID:", order.id)
        print("Status:", order.status)

        repo.delete(order)

        session.commit()

        deleted_order = repo.get_by_id(5)

        print("\nAfter delete:")
        print("Order:", deleted_order)


if __name__ == "__main__":
    
    # test_get_orders_by_buyer()
    # test_create_order()
    # test_update_order()
    # test_get_order_by_id()
    test_delete_order()