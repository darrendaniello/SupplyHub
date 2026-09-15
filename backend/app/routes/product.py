from fasthtml.common import *
from urllib.parse import quote

from app.database import SessionLocal
from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.review_service import ReviewService
from app.utils.formatter import format_rupiah

def product_routes(rt):

    @rt("/products")
    def products_page():
        session = SessionLocal()

        try:
            product_service = ProductService(session)
            category_service = CategoryService(session)

            products = product_service.get_available_products()
            categories = category_service.get_all_categories()

            product_cards = []

            for product in products:
                product_cards.append(
                    Div(
                        H3(product.name),
                        P(f"Business: {product.business.business_name}"),
                        P(f"Price: {format_rupiah(product.selling_price)} / {product.unit}"),
                        P(f"Minimum order: {product.minimum_order}"),
                        A(
                            "View detail",
                            href=f"/products/{product.id}"
                        ),
                        cls="product-card"
                    )
                )

            return Titled(
                "Products - SupplyHub",
                H1("Available Products"),
                Form(
                    Input(
                        name="keyword",
                        placeholder="Search product...",
                    ),
                    Button("Search"),
                    action="/products/search",
                    method="get",
                ),
                Form(
                    Label("Choose category"),
                    Select(
                        Option("All categories", value=""),
                        *[
                            Option(
                                category.name,
                                value=str(category.id),
                            )
                            for category in categories
                        ],
                        name="category_id",
                        onchange="this.form.submit()",
                    ),
                    action="/products/category",
                    method="get",
                ),
                Div(
                    *product_cards,
                    cls="product-list"
                )
            )

        finally:
            session.close()

    @rt("/products/search")
    def search_products_page(keyword: str=""):
        session = SessionLocal()

        try:
            product_service = ProductService(session)
            category_service = CategoryService(session)

            products = product_service.search_products(keyword)
            categories = category_service.get_all_categories()

            product_cards = []

            for product in products:
                product_cards.append(
                    Div(
                        H3(product.name),
                        P(f"Business: {product.business.business_name}"),
                        P(f"Price: {format_rupiah(product.selling_price)} / {product.unit}"),
                        A(
                            "View detail",
                            href=f"/products/{product.id}"
                        ),
                        cls="product-card",
                    )
                )

            return Titled(
                "Search Products - SupplyHub",
                H1("Search Products"),
                Form(
                    Input(
                        name="keyword",
                        value=keyword,
                        placeholder="Search product...",
                    ),
                    Button("Search"),
                    action="/products/search",
                    method="get",
                ),
                Form(
                    Label("Choose category"),
                    Select(
                        Option("All categories", value="", selected=True),
                        *[
                            Option(
                                category.name,
                                value=str(category.id),
                            )
                            for category in categories
                        ],
                        name="category_id",
                        onchange="this.form.submit()",
                    ),
                    action="/products/category",
                    method="get",
                ),
                H2(f"Search result for: {keyword}" if keyword else "All Products"),
                Div(
                    *product_cards,
                    cls="product-list",
                ),
                A("Back to products", href="/products"),
            )

        finally:
            session.close()

    @rt("/products/category")
    def products_by_category_page(category_id: int = 0):
        session = SessionLocal()

        try:
            product_service = ProductService(session)
            category_service = CategoryService(session)

            if category_id:
                products = product_service.get_products_by_category(category_id)
            else:
                products = product_service.get_available_products()

            categories = category_service.get_all_categories()

            product_cards = []

            for product in products:
                product_cards.append(
                    Div(
                        H3(product.name),
                        P(f"Business: {product.business.business_name}"),
                        P(f"Price: {format_rupiah(product.selling_price)} / {product.unit}"),
                        A(
                            "View detail",
                            href=f"/products/{product.id}",
                        ),
                        cls="product-card",
                    )
                )

            return Titled(
                "Products by Category - SupplyHub",
                H1("Products by Category"),
                Form(
                    Input(
                        name="keyword",
                        placeholder="Search products...",
                    ),
                    Button("Search"),
                    action="/products/search",
                    method="get"
                ),
                Form(
                    Label("Choose category"),
                    Select(
                        Option("All categories", value="", selected=(category_id == 0)),
                        *[
                            Option(
                                category.name,
                                value=str(category.id),
                                selected=(category.id == category_id),
                            )
                            for category in categories
                        ],
                        name="category_id",
                        onchange="this.form.submit()",
                    ),
                    action="/products/category",
                    method="get",
                ),
                Div(
                    *product_cards,
                    cls="product-list",
                ),
                A("Back to products", href="/products"),
            )

        finally:
            session.close()

    @rt("/products/{product_id}")
    def product_detail_page(product_id: int):
        session = SessionLocal()

        try:
            product_service = ProductService(session)
            review_service = ReviewService(session)

            product_result = product_service.get_product_detail(product_id)
            review_result = review_service.get_product_reviews(product_id)
            review_rating = review_service.get_product_rating(product_id)

            product = product_result["product"]
            available_quantity = product_result["available_quantity"]
            average_rating = review_rating["average_rating"] or 0
            average_rating = round(average_rating, 1)

            return Titled(
                f"{product.name} - SupplyHub",
                H1(product.name),
                P(f"Business: {product.business.business_name}"),
                P(product.description or "No description available."),
                P(f"Price: {format_rupiah(product.selling_price)} / {product.unit}"),
                P(f"Minimum order: {product.minimum_order}"),
                P(f"Available stock: {available_quantity}"),
                Form(
                    Input(
                        type="hidden",
                        name="product_id",
                        value=str(product.id),
                    ),
                    Label("Quantity"),

                    Input(
                        type="number",
                        name="quantity",
                        value=str(product.minimum_order),
                        min=str(product.minimum_order),
                        max=str(available_quantity),
                        required=True,
                    ),

                    Button("Add to Cart"),

                    action="/cart/add",
                    method="post",
                ),
                H2("Customer Reviews"),
                Div(
                    H3("Average Rating"),
                    P(
                        f"{average_rating}/5",
                        cls="average-rating-value",
                    ),
                    cls="average-rating",
                ),
                Div(
                    *[
                        Div(
                            H4(
                                f"{review.user.full_name if review.user else 'Customer'} - {review.rating}/5"
                            ),
                            P(review.comment),
                            P(
                                review.created_at.strftime("%d %B %Y")
                                if review.created_at
                                else ""
                            ),
                            cls="review-card",
                        )
                        for review in review_result
                    ],
                    cls="review-list",
                )
                if review_result
                else P("No reviews yet."),
                A("Back to products", href="/products"),
            )

        except ValueError as error:
            return Titled(
                "Product Not Found",
                H1("Product not found"),
                P(str(error)),
                A("Back to products", href="/products"),
            )

        finally:
            session.close()