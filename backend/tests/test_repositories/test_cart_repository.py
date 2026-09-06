from app.database import SessionLocal
from app.repositories.cart_repository import CartRepository


# =========================
# Cart
# =========================

def test_get_cart_by_id():
    with SessionLocal() as session:
        repository = CartRepository(session)

        cart = repository.get_cart_by_id(1)

        print("Cart:", cart)
        if cart:
            print("Cart ID:", cart.id)
            print("User ID:", cart.user_id)


def test_get_cart_by_user():
    with SessionLocal() as session:
        repository = CartRepository(session)

        cart = repository.get_cart_by_user(1)

        print("Cart:", cart)
        if cart:
            print("Cart ID:", cart.id)
            print("User ID:", cart.user_id)


# =========================
# Cart Item
# =========================

def test_get_item_by_id():
    with SessionLocal() as session:
        repository = CartRepository(session)

        item = repository.get_item_by_id(1)

        print("Cart Item:", item)
        if item:
            print("Item ID:", item.id)
            print("Cart ID:", item.cart_id)
            print("Product ID:", item.product_id)
            print("Quantity:", item.quantity)


def test_get_items_by_cart():
    with SessionLocal() as session:
        repository = CartRepository(session)

        items = repository.get_items_by_cart(1)

        print("Items:", items)

        for item in items:
            print(
                f"Item ID: {item.id}, "
                f"Product ID: {item.product_id}, "
                f"Quantity: {item.quantity}"
            )


def test_get_item_by_cart_and_product():
    with SessionLocal() as session:
        repository = CartRepository(session)

        item = repository.get_item_by_cart_and_product(
            cart_id=1,
            product_id=1,
        )

        print("Cart Item:", item)

        if item:
            print("Item ID:", item.id)
            print("Quantity:", item.quantity)


def test_create_cart():
    with SessionLocal() as session:
        repository = CartRepository(session)

        cart = repository.create_cart(
            user_id=1
        )

        session.commit()

        print("Created Cart ID:", cart.id)
        print("User ID:", cart.user_id)


def test_create_item():
    with SessionLocal() as session:
        repository = CartRepository(session)

        item = repository.create_item(
            cart_id=1,
            product_id=1,
            quantity=5,
        )

        session.commit()

        print("Created Item ID:", item.id)
        print("Cart ID:", item.cart_id)
        print("Product ID:", item.product_id)
        print("Quantity:", item.quantity)


def test_update_item():
    with SessionLocal() as session:
        repository = CartRepository(session)

        item = repository.get_item_by_id(1)

        if item is None:
            print("Cart item not found")
            return

        repository.update_item(
            cart_item=item,
            quantity=10,
        )

        session.commit()

        print("Updated Item ID:", item.id)
        print("New Quantity:", item.quantity)


def test_delete_item():
    with SessionLocal() as session:
        repository = CartRepository(session)

        item = repository.get_item_by_id(1)

        if item is None:
            print("Cart item not found")
            return

        repository.delete_item(item)

        session.commit()

        print("Deleted Cart Item ID:", item.id)


def test_delete_cart():
    with SessionLocal() as session:
        repository = CartRepository(session)

        cart = repository.get_cart_by_id(1)

        if cart is None:
            print("Cart not found")
            return

        repository.delete_cart(cart)

        session.commit()

        print("Deleted Cart ID:", cart.id)


if __name__ == "__main__":
    # test_get_cart_by_id()
    # test_get_cart_by_user()
    # test_get_item_by_id()
    # test_get_items_by_cart()
    # test_get_item_by_cart_and_product()

    # test_create_cart()
    test_create_item()

    # test_update_item()

    # test_delete_item()
    # test_delete_cart()