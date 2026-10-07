from fasthtml.common import *

from app.routes.auth import auth_routes
from app.routes.product import product_routes
from app.routes.cart import cart_routes
from app.routes.order import order_routes
from app.routes.favorite import favorite_routes
from app.routes.user_address import user_address_routes
from app.routes.ai import ai_routes
from app.routes.business import business_routes

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
        A("My Favorites", href="/favorites"),
        Br(),
        A("User Addresses", href="/profile/addresses"),
        Br(),
        A("AI Forecast", href="/ai/forecast"),
        Br(),
        A("Business Nearby", href="/businesses/nearby"),
        Br(),
        A("Logout", href="/logout"),
    )


auth_routes(rt)
product_routes(rt)
cart_routes(rt)
order_routes(rt)
favorite_routes(rt)
user_address_routes(rt)
ai_routes(rt)
business_routes(rt)