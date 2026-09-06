from app.database import SessionLocal
from app.services.cart_service import CartService

def test_get_cart():
    with SessionLocal() as session:
        service = CartService(session)

        result = service.get_cart(user_id=1)

        cart = result["cart"]
        items = result["items"]

        print("Cart ID:", cart.id)
        print("User ID:", cart.user_id)
        print("Items:")

        for item in items:
            print(
                f"Item ID: {item.id}, "
                f"Product ID: {item.product_id}, "
                f"Quantity: {item.quantity}"
            )

def test_add_to_cart():
    with SessionLocal() as session:
        service = CartService(session)

        item = service.add_to_cart(
            user_id=1,
            product_id=2,
            quantity=10,
        )

        session.commit()

        print("Cart item ID:", item.id)
        print("Cart ID:", item.cart_id)
        print("Product ID:", item.product_id)
        print("Quantity:", item.quantity)

def test_update_cart_item():
    with SessionLocal() as session:
        service = CartService(session)

        item = service.update_cart_item(
            user_id=1,
            cart_item_id=1,
            quantity=10,
        )

        session.commit()

        print("Updated Cart Item ID:", item.id)
        print("Cart ID:", item.cart_id)
        print("Product ID:", item.product_id)
        print("New Quantity:", item.quantity)

def test_remove_from_cart():
    with SessionLocal() as session:
        service = CartService(session)

        service.remove_from_cart(
            user_id=1,
            cart_item_id=1,
        )

        session.commit()

        print("Cart item removed successfully")

def test_clear_cart():
    with SessionLocal() as session:
        service = CartService(session)

        # Tambahkan beberapa item ke cart
        service.add_to_cart(
            user_id=1,
            product_id=1,
            quantity=2,
        )

        service.add_to_cart(
            user_id=1,
            product_id=3,
            quantity=5,
        )

        session.commit()

        # Clear semua item
        service.clear_cart(user_id=1)

        session.commit()

        print("Cart cleared successfully")

if __name__ == "__main__":
    test_get_cart()
    # test_add_to_cart()
    # test_update_cart_item()
    # test_remove_from_cart()
    # test_clear_cart()