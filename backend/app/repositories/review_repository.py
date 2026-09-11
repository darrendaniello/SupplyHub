from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.models import Review

class ReviewRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, review_id: int):
        stmt = select(Review).where(
            Review.id == review_id
        )

        return self.session.scalar(stmt)

    def get_by_product(self, product_id: int):
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
        )

        return self.session.scalars(stmt).all()
    
    def get_average_rating(self, product_id: int):
        stmt = (
            select(func.avg(Review.rating))
            .where(Review.product_id == product_id)
        )

        return self.session.scalar(stmt)

    def get_review_count(self, product_id: int):
        stmt = (
            select(func.count(Review.id))
            .where(Review.product_id == product_id)
        )

        return self.session.scalar(stmt)

    def get_by_user_and_by_product(self, user_id: int, product_id: int):
        stmt = (
            select(Review)
            .where(
                Review.user_id == user_id,
                Review.product_id == product_id
            )
        )

        return self.session.scalar(stmt)

    def create(
            self,
            product_id: int,
            user_id: int,
            rating: int,
            comment: str | None = None
    ):
        review = Review(
            product_id = product_id,
            user_id = user_id,
            rating = rating,
            comment = comment
        )

        self.session.add(review)
        self.session.flush()

        return review

    def delete(self, review: Review):
        self.session.delete(review)
        self.session.flush()