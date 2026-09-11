from fasthtml.common import *

from app.database import SessionLocal
from app.services.cart_service import CartService


def cart_routes(rt):

    @rt("/cart")
    def cart_page(request):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return Titled(
                    "Login Required - SupplyHub",
                    H1("Login required"),
                    P("Please login before viewing your cart."),
                    A("Go to login", href="/login"),
                )

            cart_service = CartService(session)

            cart_result = cart_service.get_cart(int(user_id))
            items = cart_result["items"]

            cart_items = []

            for item in items:
                cart_items.append(
                    Div(
                        H3(f"Product ID: {item.product_id}"),
                        P(f"Quantity: {item.quantity}"),
                        cls="cart-item",
                    )
                )

            return Titled(
                "My Cart - SupplyHub",
                H1("My Cart"),
                Div(
                    *cart_items,
                    cls="cart-list",
                )
                if cart_items
                else P("Your cart is empty."),
                A("Continue shopping", href="/products"),
            )

        finally:
            session.close()

    @rt("/cart/add", methods=["post"])
    def add_to_cart(
        request,
        product_id: int,
        quantity: int,
    ):
        print("POST /cart/add")
        print("PRODUCT ID:", product_id)
        print("QUANTITY:", quantity)

        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return Titled(
                    "Login Required - SupplyHub",
                    H1("Login required"),
                    A("Go to login", href="/login"),
                )

            cart_service = CartService(session)

            cart_service.add_to_cart(
                user_id=int(user_id),
                product_id=product_id,
                quantity=quantity,
            )

            session.commit()

            return RedirectResponse(
                "/cart",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Add to Cart Failed - SupplyHub",
                H1("Unable to add product to cart"),
                P(str(error)),
                A("Back to products", href="/products"),
            )

        except Exception as error:
            session.rollback()

            print("ADD TO CART ERROR:", repr(error))

            return Titled(
                "Add to Cart Failed - SupplyHub",
                H1("Unable to add product to cart"),
                P(str(error)),
                A("Back to products", href="/products"),
            )

        finally:
            session.close()