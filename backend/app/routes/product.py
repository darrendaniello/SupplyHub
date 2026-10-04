from fasthtml.common import *
from urllib.parse import quote

from app.database import SessionLocal
from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.review_service import ReviewService
from app.utils.formatter import format_rupiah

def product_routes(rt):

    @rt("/products")
    def products_page(
        keyword: str = "",
        category_id: str = "",
        min_price: str = "",
        max_price: str = "",
        min_rating: str = "",
        sort_by: str = "",
    ):
        session = SessionLocal()

        try:
            product_service = ProductService(session)
            category_service = CategoryService(session)

            parsed_category_id = int(category_id) if category_id else None
            parsed_min_price = float(min_price) if min_price else None
            parsed_max_price = float(max_price) if max_price else None
            parsed_min_rating = float(min_rating) if min_rating else None

            products = product_service.filter_products(
                keyword=keyword,
                category_id=parsed_category_id,
                min_price=parsed_min_price,
                max_price=parsed_max_price,
                min_rating=parsed_min_rating,
                sort_by=sort_by or None,
            )

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
                        value=keyword,
                    ),

                    Label("Category"),
                    Select(
                        Option(
                            "All categories",
                            value="",
                            selected=(category_id == ""),
                        ),
                        *[
                            Option(
                                category.name,
                                value=str(category.id),
                                selected=(category_id == str(category.id)),
                            )
                            for category in categories
                        ],
                        name="category_id",
                    ),

                    Label("Minimum price"),
                    Input(
                        type="number",
                        name="min_price",
                        placeholder="Minimum price",
                        value=min_price,
                        min="0",
                    ),

                    Label("Maximum price"),
                    Input(
                        type="number",
                        name="max_price",
                        placeholder="Maximum price",
                        value=max_price,
                        min="0",
                    ),

                    Label("Minimum rating"),
                    Select(
                        Option(
                            "All ratings",
                            value="",
                            selected=(min_rating == ""),
                        ),
                        Option(
                            "4+ stars",
                            value="4",
                            selected=(min_rating == "4"),
                        ),
                        Option(
                            "5 stars",
                            value="5",
                            selected=(min_rating == "5"),
                        ),
                        name="min_rating",
                    ),

                    Label("Sort by"),
                    Select(
                        Option(
                            "Name",
                            value="",
                            selected=(sort_by == ""),
                        ),
                        Option(
                            "Price: Low to High",
                            value="price_asc",
                            selected=(sort_by == "price_asc"),
                        ),
                        Option(
                            "Price: High to Low",
                            value="price_desc",
                            selected=(sort_by == "price_desc"),
                        ),
                        Option(
                            "Highest Rating",
                            value="rating",
                            selected=(sort_by == "rating"),
                        ),
                        name="sort_by",
                    ),

                    Button("Apply Filters", type="submit"),

                    action="/products",
                    method="get",
                ),
                Div(
                    *product_cards,
                    cls="product-list"
                )
            ),

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

    @rt("/products/{product_id}", methods=["GET"])
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

                H2("Write a Review"),

                Form(
                    Label("Rating"),
                    Input(
                        type="number",
                        name="rating",
                        min="1",
                        max="5",
                        required=True,
                    ),

                    Label("Comment"),
                    Textarea(
                        name="comment",
                        placeholder="Write your review...",
                    ),

                    Button(
                        "Submit Review",
                        type="submit",
                    ),

                    action=f"/products/{product.id}/reviews",
                    method="post",
                ),

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

    @rt("/products/{product_id}/reviews", methods=["POST"])
    def create_product_reviews(
        request,
        product_id: int,
        rating: int,
        comment: str = "",
    ):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            review_service = ReviewService(session)

            review_service.create_review(
                user_id=int(user_id),
                product_id=product_id,
                rating=rating,
                comment=comment,
            )

            session.commit()

            return RedirectResponse(
                f"/products/{product_id}",
                status_code=303,
            )
        
        except ValueError as error:
            session.rollback()

            return Titled(
                "Review Error - SupplyHub",
                H1("Unable to Submit Review"),
                P(str(error)),
                A(
                    "Back to Product",
                    href=f"/products/{product_id}",
                ),
            )
        
        except Exception as error:
            session.rollback()

            print("CREATE REVIEW ERROR: ", repr(error))

            return Titled(
               "Review Error - SupplyHub",
                H1("Something went wrong"),
                P("Unable to submit your review."),
                A(
                    "Back to Product",
                    href=f"/products/{product_id}",
                ), 
            )
        
        finally:
            session.close()