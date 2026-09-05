from app.database import SessionLocal
from app.services.favorite_service import FavoriteService

def test_add_favorite():
    with SessionLocal() as session:
        service = FavoriteService(session)

        favorite = service.add_favorite(
            user_id=1,
            product_id=1,
        )

        session.commit()

        print("\nFvorite created:")
        print("ID:", favorite.id)
        print("User ID:", favorite.user_id)
        print("Product ID:", favorite.product_id)

def test_is_favorite():
    with SessionLocal() as session:
        service = FavoriteService(session)

        result = service.is_favorite(
            user_id=1,
            product_id=1,
        )

        print("\nIs favorite:", result)

def test_duplicate_favorite():
    with SessionLocal() as session:
        service = FavoriteService(session)

        try:
            service.add_favorite(
                user_id=1,
                product_id=1,
            )
        except ValueError as e:
            print("\nDuplicate favorite blocked:")
            print(e)

def test_remove_favorite():
    with SessionLocal() as session:
        service = FavoriteService(session)

        service.remove_favorite(
            user_id=1,
            product_id=1,
        )

        session.commit()

        print("\nFavorite removed successfully!")


if __name__ == "__main__":
    test_add_favorite()
    test_is_favorite()
    test_duplicate_favorite()
    test_remove_favorite()