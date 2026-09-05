from app.database import SessionLocal
from app.repositories.order_item_repository import OrderItemRepository
from decimal import Decimal

def test_get_order_item_by_id():
    with SessionLocal() as session:
        repo = OrderItemRepository(session)

        order_item = repo.get_by_id(1)

        if order_item is None:
            print("\nOrder item not found.")
            return

        print("\nOrder item found:")
        print("Order Item ID:", order_item.id)
        print("Order ID:", order_item.order_id)
        print("Product ID:", order_item.product_id)
        print("Quantity:", order_item.quantity)
        print("Unit Price:", order_item.unit_price)
        print("Subtotal:", order_item.subtotal)

def test_get_order_items_by_order():
    with SessionLocal() as session:
        repo = OrderItemRepository(session)

        order_items = repo.get_by_order(2)

        print("\nOrder items found:", len(order_items))

        for item in order_items:
            print(
                f"Order Item ID: {item.id}, "
                f"Order ID: {item.order_id}, "
                f"Product ID: {item.product_id}, "
                f"Quantity: {item.quantity}, "
                f"Unit Price: {item.unit_price}, "
                f"Subtotal: {item.subtotal}"
            )

def test_get_order_items_by_product():
    with SessionLocal() as session:
        repository = OrderItemRepository(session)

        order_items = repository.get_by_product(3)

        print("\nOrder items found:", len(order_items))

        for item in order_items:
            print(
                f"Order Item ID: {item.id}, "
                f"Order ID: {item.order_id}, "
                f"Product ID: {item.product_id}, "
                f"Quantity: {item.quantity}, "
                f"Unit Price: {item.unit_price}, "
                f"Subtotal: {item.subtotal}"
            )

def test_create_order_item():
    with SessionLocal() as session:
        repository = OrderItemRepository(session)

        order_item = repository.create(
            order_id=1,
            product_id=1,
            quantity=10,
            unit_price=Decimal("15000.00"),
            subtotal=Decimal("150000.00"),
        )

        session.commit()

        print("\nOrder item created successfully!")
        print("Order Item ID:", order_item.id)
        print("Order ID:", order_item.order_id)
        print("Product ID:", order_item.product_id)
        print("Quantity:", order_item.quantity)
        print("Unit Price:", order_item.unit_price)
        print("Subtotal:", order_item.subtotal)

def test_update_order_item():
    with SessionLocal() as session:
        repository = OrderItemRepository(session)

        order_item = repository.get_by_id(1)

        if order_item is None:
            print("\nOrder item not found.")
            return

        print("\nBefore update:")
        print("Order Item ID:", order_item.id)
        print("Quantity:", order_item.quantity)
        print("Unit Price:", order_item.unit_price)
        print("Subtotal:", order_item.subtotal)

        updated_item = repository.update(
            order_item=order_item,
            quantity=20,
            unit_price=Decimal("15000.00"),
            subtotal=Decimal("300000.00"),
        )

        session.commit()

        print("\nAfter update:")
        print("Order Item ID:", updated_item.id)
        print("Quantity:", updated_item.quantity)
        print("Unit Price:", updated_item.unit_price)
        print("Subtotal:", updated_item.subtotal)

def test_delete_order_item():
    with SessionLocal() as session:
        repository = OrderItemRepository(session)

        order_item = repository.get_by_id(31)

        if order_item is None:
            print("\nOrder item not found.")
            return

        print("\nBefore delete:")
        print("Order Item ID:", order_item.id)
        print("Order ID:", order_item.order_id)
        print("Product ID:", order_item.product_id)

        repository.delete(order_item)

        session.commit()

        deleted_item = repository.get_by_id(31)

        print("\nAfter delete:")
        print("Order Item:", deleted_item)

if __name__ == "__main__":
    # test_get_order_item_by_id()
    # test_get_order_items_by_order()
    # test_get_order_items_by_product()
    # test_create_order_item()
    # test_update_order_item()
    test_delete_order_item()