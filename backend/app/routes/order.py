from fasthtml.common import *
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.utils.formatter import format_rupiah
from app.services.order_service import OrderService

def order_routes(rt):

    @rt("/orders")
    def order_list(request):
        session: Session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            order_service = OrderService(session)
            orders = order_service.get_user_orders(int(user_id))

            order_lists = []

            for order in orders:
                order_lists.append(
                    Tr(
                        Td(f"#{order.id}"),
                        Td(order.status),
                        Td(f"Rp {order.total_amount:,.0f}"),
                        Td(str(order.created_at)),
                        Td(
                            A(
                                "View Detail",
                                href=f"/orders/{order.id}",
                            )
                        ),
                    )
                )

            return Titled(
                "My Orders",
                H1("My Orders"),
                Table(
                    Thead(
                        Tr(
                            Th("Order"),
                            Th("Status"),
                            Th("Total"),
                            Th("Created At"),
                            Th("Action"),
                        )
                    ),
                    Tbody(*order_lists),
                ),
                A("Continue Shopping", href="/products"),
            )

        finally:
            session.close()

    @rt("/orders/{order_id}")
    def order_detail(request, order_id: int):
        session: Session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303
                )

            order_service = OrderService(session)

            result = order_service.get_order_detail(
                user_id=int(user_id),
                order_id=order_id,
            )

            order = result["order"]
            items = result["items"]

            item_lists = []

            for item in items:
                item_lists.append(
                    Tr(
                        Td(item.product.name),
                        Td(str(item.quantity)),
                        Td(format_rupiah(item.unit_price)),
                        Td(format_rupiah(item.subtotal)),
                    )
                )

            return Titled(
                f"Order #{order.id}",
                H1(f"Order #{order.id}"),
                P(
                    Strong("Order status: "),
                    order.status
                ),
                P(
                    Strong("Created at: "),
                    str(order.created_at),
                ),
                P(
                    Strong("Shipping address: "),
                    order.shipping_address,
                ),
                P(
                    Strong("Supplier: "),
                    order.supplier_business.business_name
                    if order.supplier_business
                    else "Supplier unavailable"
                ),

                H2("order Items"),

                Table(
                    Thead(
                        Tr(
                            Th("Product"),
                            Th("Quantity"),
                            Th("Unit Price"),
                            Th("Subtotal"),
                        )
                    ),
                    Tbody(*item_lists),
                ),
                H3(
                    Strong(
                        f"Total: {format_rupiah(order.total_amount)}"
                    ),
                ),

                Br(),

                A("Back to orders", href="/orders"),

                Br(),

                A("Continue shopping", href="/products"),
            )

        except ValueError as error:
            return Titled(
                "Order error",
                H1("Unable to open order"),
                P(str(error)),
                A("Back to orders", href="/orders"),
            )

        finally:
            session.close()