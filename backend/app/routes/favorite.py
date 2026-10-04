from fasthtml.common import *

from app.database import SessionLocal
from app.services.favorite_service import FavoriteService
from app.utils.formatter import format_rupiah


def favorite_routes(rt):

    @rt("/favorites")
    def favorite_page(request):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            favorite_service = FavoriteService(session)

            favorites = favorite_service.get_user_favorites(
                user_id=int(user_id)
            )

            favorite_cards = []

            for favorite in favorites:
                product = favorite.product

                favorite_cards.append(
                    Div(
                        H3(product.name),

                        P(
                            f"Business: "
                            f"{product.business.business_name}"
                        ),

                        P(
                            f"Price: "
                            f"{format_rupiah(product.selling_price)} "
                            f"/ {product.unit}"
                        ),

                        P(
                            f"Minimum order: "
                            f"{product.minimum_order}"
                        ),

                        A(
                            "View product",
                            href=f"/products/{product.id}",
                        ),

                        Form(
                            Button(
                                "Remove from Favorites",
                                type="submit",
                            ),
                            action=f"/favorites/{product.id}/remove",
                            method="post",
                        ),

                        cls="favorite-card",
                    )
                )

            return Titled(
                "My Favorites - SupplyHub",

                H1("My Favorites"),

                Div(
                    *favorite_cards,
                    cls="favorite-list",
                )
                if favorite_cards
                else P(
                    "You don't have any favorite products yet."
                ),

                A(
                    "Back to products",
                    href="/products",
                ),
            )

        finally:
            session.close()

    @rt("/products/{product_id}/favorite", methods=["POST"])
    def add_favorite(request, product_id: int):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            favorite_service = FavoriteService(session)

            favorite_service.add_favorite(
                user_id=int(user_id),
                product_id=product_id,
            )

            session.commit()

            return RedirectResponse(
                f"/products/{product_id}",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Favorite Error - SupplyHub",
                H1("Unable to Add Favorite"),
                P(str(error)),
                A(
                    "Back to Product",
                    href=f"/products/{product_id}",
                ),
            )

        except Exception as error:
            session.rollback()

            print("ADD FAVORITE ERROR:", repr(error))

            return Titled(
                "Favorite Error - SupplyHub",
                H1("Something went wrong"),
                P("Unable to add product to favorites."),
                A(
                    "Back to Product",
                    href=f"/products/{product_id}",
                ),
            )

        finally:
            session.close()

    @rt("/products/{product_id}/favorite/remove", methods=["POST"])
    def remove_favorite(request, product_id: int):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse(
                    "/login",
                    status_code=303,
                )

            favorite_service = FavoriteService(session)

            favorite_service.remove_favorite(
                user_id=int(user_id),
                product_id=product_id,
            )

            session.commit()

            return RedirectResponse(
                f"/products/{product_id}",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Favorite Error - SupplyHub",
                H1("Unable to Remove Favorite"),
                P(str(error)),
                A(
                    "Back to Product",
                    href=f"/products/{product_id}",
                ),
            )

        except Exception as error:
            session.rollback()

            print("REMOVE FAVORITE ERROR:", repr(error))

            return Titled(
                "Favorite Error - SupplyHub",
                H1("Something went wrong"),
                P("Unable to remove product from favorites."),
                A(
                    "Back to Product",
                    href=f"/products/{product_id}",
                ),
            )

        finally:
            session.close()

    @rt("/favorites/{product_id}/remove", methods=["POST"])
    def remove_favorite_from_list(request, product_id: int):
        session = SessionLocal()

        try:
            user_id = request.session.get("user_id")

            if not user_id:
                return RedirectResponse("/login", status_code=303)

            favorite_service = FavoriteService(session)

            favorite_service.remove_favorite(
                user_id=int(user_id),
                product_id=product_id,
            )

            session.commit()

            return RedirectResponse(
                "/favorites",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Favorite Error - SupplyHub",
                H1("Unable to Remove Favorite"),
                P(str(error)),
                A(
                    "Back to Favorites",
                    href="/favorites",
                ),
            )

        except Exception as error:
            session.rollback()
            print("REMOVE FAVORITE FROM LIST ERROR:", repr(error))

            return Titled(
                "Favorite Error - SupplyHub",
                H1("Something went wrong"),
                P("Unable to remove product from favorites."),
                A(
                    "Back to Favorites",
                    href="/favorites",
                ),
            )

        finally:
            session.close()