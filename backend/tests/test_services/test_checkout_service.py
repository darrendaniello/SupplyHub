from app.database import SessionLocal
from app.services.cart_service import CartService
from app.services.checkout_service import CheckoutService

def test_checkout():
    with SessionLocal() as session:
        service = CheckoutService(session)
        cart_service = CartService(session)

         # Tambahkan produk ke cart 
        cart_service.add_to_cart(
            user_id=1,
            product_id=1,
            quantity=1,
        )

        result = service.checkout(user_id=1)

        session.commit()

        print("Checkout successful")
        print("Total amount:", result["total_amount"])

        print("Orders:")

        for order in result["orders"]:
            print(
                f"Order ID: {order.id}, "
                f"Supplier Business ID: {order.supplier_business_id}, "
                f"Total: {order.total_amount}, "
                f"Status: {order.status}"
            )


if __name__ == "__main__":
    test_checkout()