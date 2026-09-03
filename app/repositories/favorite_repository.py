from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.favorite import Favorite


class FavoriteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, favorite_id: int):
        stmt = (
            select(Favorite)
            .where(Favorite.id == favorite_id)
        )

        return self.session.scalar(stmt)

    def get_by_user(self, user_id: int):
        stmt = (
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )

        return self.session.scalars(stmt).all()

    def get_by_user_and_product(
        self,
        user_id: int,
        product_id: int,
    ):
        stmt = (
            select(Favorite)
            .where(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id,
            )
        )

        return self.session.scalar(stmt)

    def create(
        self,
        user_id: int,
        product_id: int,
    ):
        favorite = Favorite(
            user_id=user_id,
            product_id=product_id,
        )

        self.session.add(favorite)
        self.session.flush()

        return favorite

    def delete(self, favorite: Favorite):
        self.session.delete(favorite)
        self.session.flush()