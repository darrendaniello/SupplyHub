from fasthtml.common import *

from app.database import SessionLocal
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.utils.formatter import format_rupiah


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

            total = 0

            for item in items:
                product = item.product

                subtotal = product.selling_price * item.quantity

                total += subtotal

                cart_items.append(
                    Div(
                        Input(
                            type="checkbox",
                            name="cart_item_id",
                            value=str(item.id),
                            form="checkout-form",
                        ),
                        H3(product.name),
                        P(
                            f"Business: {item.product.business.business_name}"
                        ),
                        P(
                            f"Price: {format_rupiah(product.selling_price)} / {product.unit}"
                        ),
                        P(f"Quantity: {item.quantity}"),
                        P(f"Subtotal: {format_rupiah(subtotal)}"),
                        Div(
                            Form(
                                Input(
                                    type="hidden",
                                    name="cart_item_id",
                                    value=str(item.id),
                                ),
                                Input(
                                    type="number",
                                    name="quantity",
                                    value=str(item.quantity),
                                    min="1",
                                    required=True,
                                ),
                                Button("Update quantity"),
                                action="/cart/update",
                                method="post",
                            ),
                            Form(
                                Input(
                                    type="hidden",
                                    name="cart_item_id",
                                    value=str(item.id),
                                ),
                                Button("Remove", type="submit"),
                                action="/cart/remove",
                                method="post",
                            ),
                            cls="cart-action",
                        ),
                        cls="cart-item",
                    ),
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

                Hr(),

                P(
                    f"Total: {format_rupiah(total)}",
                    cls="cart-total",
                )
                if cart_items
                else None,

                Form(
                    Button(
                        "Checkout selected items",
                        type="submit",
                    ),
                    action="/checkout",
                    method="get",
                    id="checkout-form",
                )
                if cart_items
                else None,

                Br(),
                A("My Orders", href="/orders"),
                Br(),
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

    @rt("/cart/update", methods=["post"])
    def update_cart(
        request,
        cart_item_id: int,
        quantity: int,
    ):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            cart_service = CartService(session)

            cart_service.update_cart_item(
                user_id=int(user_id),
                cart_item_id=cart_item_id,
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
                "Update cart failed - SupplyHub",
                H1("Unable to update cart"),
                P(str(error)),
                A("Back to cart", href="/cart"),
            )

        except Exception as error:
            session.rollback()

            return Titled(
                "Update Cart Failed - SupplyHub",
                H1("Unable to update cart"),
                P("Something went wrong while updating your cart."),
                A("Back to cart", href="/cart"),
            )

        finally:
            session.close()

    @rt("/cart/remove", methods=["post"])
    def remove_cart_item(
        request,
        cart_item_id: int,
    ):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            cart_service = CartService(session)

            cart_service.remove_from_cart(
                user_id=int(user_id),
                cart_item_id=cart_item_id,
            )

            session.commit()

            return RedirectResponse(
                "/cart",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Remove Cart Item Failed - SupplyHub",
                H1("Unable to remove item"),
                P(str(error)),
                A("Back to cart", href="/cart"),
            )

        except Exception as error:
            session.rollback()

            print("REMOVE CART ITEM ERROR:", repr(error))

            return Titled(
                "Remove Cart Item Failed - SupplyHub",
                H1("Unable to remove item"),
                P("Something went wrong while removing the item."),
                A("Back to cart", href="/cart"),
            )

        finally:
            session.close()

    @rt("/checkout", methods=["GET"])
    def checkout_page(request):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            # =========================
            # Get selected cart items
            # =========================

            selected_item_ids = request.query_params.getlist(
                "cart_item_id"
            )

            if not selected_item_ids:
                return Titled(
                    "Checkout - SupplyHub",
                    H1("No Items Selected"),
                    P(
                        "Please select at least one item "
                        "from your cart."
                    ),
                    A(
                        "Back to cart",
                        href="/cart",
                    ),
                )

            try:
                selected_item_ids = [
                    int(item_id)
                    for item_id in selected_item_ids
                ]
            except ValueError:
                return Titled(
                    "Checkout - SupplyHub",
                    H1("Invalid Selection"),
                    P(
                        "Invalid cart item selection."
                    ),
                    A(
                        "Back to cart",
                        href="/cart",
                    ),
                )

            # =========================
            # Get user's cart
            # =========================

            cart_service = CartService(session)

            cart = cart_service.cart_repository.get_cart_by_user(
                int(user_id)
            )

            if cart is None:
                return Titled(
                    "Checkout - SupplyHub",
                    H1("Your cart is empty"),
                    P(
                        "Add products to your cart "
                        "before checkout."
                    ),
                    A(
                        "Continue shopping",
                        href="/products",
                    ),
                )

            # =========================
            # Get selected items
            # =========================

            cart_items = cart_service.cart_repository.get_items_by_ids(
                cart.id,
                selected_item_ids,
            )

            if not cart_items:
                return Titled(
                    "Checkout - SupplyHub",
                    H1("Selected items not found"),
                    P(
                        "The selected cart items "
                        "could not be found."
                    ),
                    A(
                        "Back to cart",
                        href="/cart",
                    ),
                )

            # =========================
            # Calculate total
            # =========================

            total = 0
            checkout_items = []

            for item in cart_items:
                product = item.product

                if product is None:
                    continue

                subtotal = (
                    product.selling_price * item.quantity
                )

                total += subtotal

                checkout_items.append(
                    Div(
                        H3(product.name),

                        P(
                            f"Business: "
                            f"{product.business.business_name}"
                        ),

                        P(
                            f"Quantity: {item.quantity}"
                        ),

                        P(
                            f"Subtotal: "
                            f"{format_rupiah(subtotal)}"
                        ),
                    )
                )

            # =========================
            # Checkout page
            # =========================

            return Titled(
                "Checkout - SupplyHub",

                H1("Checkout"),

                H2("Order Summary"),

                Div(
                    *checkout_items,

                    Hr(),

                    P(
                        f"Total: "
                        f"{format_rupiah(total)}",
                        cls="checkout-total",
                    ),
                ),

                H2("Shipping Address"),

                Form(
                    Label(
                        "Shipping Address",
                        for_="shipping_address",
                    ),

                    Textarea(
                        name="shipping_address",
                        id="shipping_address",
                        required=True,
                        placeholder="Enter your shipping address",
                    ),

                    # Preserve selected cart items
                    Input(
                        type="hidden",
                        name="selected_item_ids",
                        value=",".join(map(str, selected_item_ids)),
                    ),

                    Button(
                        "Place Order",
                        type="submit",
                    ),

                    action="/checkout",
                    method="post",
                ),

                Br(),

                A(
                    "Back to cart",
                    href="/cart",
                ),

                Br(),

                A(
                    "My Orders",
                    href="/orders",
                ),
            )

        finally:
            session.close()

    @rt("/checkout", methods=["POST"])
    def checkout_submit(
        request,
        shipping_address: str,
        selected_item_ids: str,
    ):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            try:
                cart_item_ids = [
                    int(item_id)
                    for item_id in selected_item_ids.split(",")
                    if item_id
                ]
            except ValueError:
                return Titled(
                    "Checkout error - SupplyHub",
                    H1("Checkout failed"),
                    P("Invalid cart item selection."),
                    A("Back to cart", href="/cart"),
                )

            if not cart_item_ids:
                return Titled(
                    "Checkout Error - SupplyHub",
                    H1("Checkout failed"),
                    P("No cart items selected."),
                    A("Back to cart", href="/cart"),
                )

            order_service = OrderService(session)

            order = order_service.create_order(
                user_id=int(user_id),
                shipping_address=shipping_address,
                cart_item_ids=cart_item_ids,
            )

            session.commit()

            return RedirectResponse(
                "/orders",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Checkout Error",
                H1("Checkout failed"),
                P(str(error)),
                A("Back to checkout", href="/checkout"),
            )

        except Exception as error:
            session.rollback()

            print("CHECKOUT ERROR:", repr(error))

            return Titled(
                "Checkout Error",
                H1("Something went wrong"),
                P("Unable to place your order."),
                A("Back to checkout", href="/checkout"),
            )

        finally:
            session.close()