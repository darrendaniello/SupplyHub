from app.database import SessionLocal
from app.repositories.favorite_repository import FavoriteRepository


def test_get_favorite_by_id():
    with SessionLocal() as session:
        repository = FavoriteRepository(session)

        favorite = repository.get_by_id(1)

        if favorite is None:
            print("Favorite not found")
            return

        print(f"Favorite ID: {favorite.id}")
        print(f"User ID: {favorite.user_id}")
        print(f"Product ID: {favorite.product_id}")


def test_get_favorites_by_user():
    with SessionLocal() as session:
        repository = FavoriteRepository(session)

        favorites = repository.get_by_user(1)

        print(f"Total favorites: {len(favorites)}")

        for favorite in favorites:
            print(
                f"Favorite ID: {favorite.id} | "
                f"Product ID: {favorite.product_id}"
            )


def test_get_favorite_by_user_and_product():
    with SessionLocal() as session:
        repository = FavoriteRepository(session)

        favorite = repository.get_by_user_and_product(
            user_id=1,
            product_id=1,
        )

        if favorite is None:
            print("Favorite not found")
        else:
            print(f"Favorite ID: {favorite.id}")


def test_create_favorite():
    with SessionLocal() as session:
        repository = FavoriteRepository(session)

        favorite = repository.create(
            user_id=1,
            product_id=1,
        )

        session.commit()

        print(f"Created favorite ID: {favorite.id}")


def test_delete_favorite():
    with SessionLocal() as session:
        repository = FavoriteRepository(session)

        favorite = repository.get_by_user_and_product(
            user_id=1,
            product_id=1,
        )

        if favorite is None:
            print("Favorite not found")
            return

        repository.delete(favorite)

        session.commit()

        print("Favorite deleted")


if __name__ == "__main__":
    test_get_favorite_by_id()
    test_get_favorites_by_user()
    test_get_favorite_by_user_and_product()
    
    # test_create_favorite()

    # test_delete_favorite()