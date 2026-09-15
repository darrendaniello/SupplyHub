from fasthtml.common import *

from app.routes.auth import auth_routes
from app.routes.product import product_routes
from app.routes.cart import cart_routes
from app.routes.order import order_routes


app, rt = fast_app(secret_key="supplyhub-secret-key")


@rt("/")
def home():
    return Titled(
        "SupplyHub",
        H1("SupplyHub"),
        P("Supply chain marketplace untuk buyer."),
        A("Register", href="/register"),
        Br(),
        A("Login", href="/login"),
        Br(),
        A("Products", href="/products"),
        Br(),
        A("Cart", href="/cart"),
        Br(),
        A("Orders", href="/orders"),
        Br(),
        A("Logout", href="/logout"),
    )


auth_routes(rt)
product_routes(rt)
cart_routes(rt)
order_routes(rt)