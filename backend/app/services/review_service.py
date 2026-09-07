from sqlalchemy.orm import Session

from app.repositories.review_repository import ReviewRepository


class ReviewService:
    def __init__(self, session: Session):
        self.review_repository = ReviewRepository(session)

    def get_product_reviews(self, product_id: int):
        return self.review_repository.get_by_product(product_id)

    def get_product_rating(self, product_id: int):
        average_rating = self.review_repository.get_average_rating(product_id)
        review_count = self.review_repository.get_review_count(product_id)

        return {
            "average_rating": average_rating,
            "review_count": review_count,
        }

    def create_review(
        self,
        user_id: int,
        product_id: int,
        rating: int,
        comment: str | None = None,
    ):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        existing_review = (
            self.review_repository.get_by_user_and_by_product(
                user_id=user_id,
                product_id=product_id,
            )
        )

        if existing_review is not None:
            raise ValueError(
                "User has already reviewed this product"
            )

        if comment is not None:
            comment = comment.strip()

        return self.review_repository.create(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
        )

    def delete_review(self, user_id: int, review_id: int):
        review = self.review_repository.get_by_id(review_id)

        if review is None:
            raise ValueError("Review not found")

        if review.user_id != user_id:
            raise ValueError(
                "Review does not belong to this user"
            )

        self.review_repository.delete(review)