from sqlalchemy.orm import Session

from app.repositories.favorite_repository import FavoriteRepository


class FavoriteService:
    def __init__(self, session: Session):
        self.favorite_repository = FavoriteRepository(session)

    def get_user_favorites(self, user_id: int):
        return self.favorite_repository.get_by_user(user_id)

    def add_favorite(self, user_id: int, product_id: int):
        existing_favorite = (
            self.favorite_repository
            .get_by_user_and_product(user_id, product_id)
        )

        if existing_favorite is not None:
            raise ValueError("Product is already in favorites")

        return self.favorite_repository.create(
            user_id=user_id,
            product_id=product_id,
        )

    def remove_favorite(self, user_id: int, product_id: int):
        favorite = (
            self.favorite_repository
            .get_by_user_and_product(user_id, product_id)
        )

        if favorite is None:
            raise ValueError("Favorite not found")

        self.favorite_repository.delete(favorite)

    def is_favorite(self, user_id: int, product_id: int):
        favorite = (
            self.favorite_repository
            .get_by_user_and_product(user_id, product_id)
        )

        return favorite is not None