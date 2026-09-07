from app.database import SessionLocal
from app.services.review_service import ReviewService


def test_create_review():
    with SessionLocal() as session:
        service = ReviewService(session)

        review = service.create_review(
            user_id=1,
            product_id=1,
            rating=5,
            comment="Produk bagus dan sesuai kebutuhan.",
        )

        session.commit()

        print("Review created successfully")
        print("Review ID:", review.id)
        print("User ID:", review.user_id)
        print("Product ID:", review.product_id)
        print("Rating:", review.rating)
        print("Comment:", review.comment)

def test_get_product_reviews():
    with SessionLocal() as session:
        service = ReviewService(session)

        reviews = service.get_product_reviews(product_id=1)

        print("Product Reviews:")

        for review in reviews:
            print(
                f"Review ID: {review.id}, "
                f"User ID: {review.user_id}, "
                f"Rating: {review.rating}, "
                f"Comment: {review.comment}"
            )


def test_get_product_rating():
    with SessionLocal() as session:
        service = ReviewService(session)

        result = service.get_product_rating(product_id=1)

        print("\nProduct Rating:")
        print("Average Rating:", result["average_rating"])
        print("Review Count:", result["review_count"])

def test_duplicate_review():
    with SessionLocal() as session:
        service = ReviewService(session)

        try:
            service.create_review(
                user_id=1,
                product_id=1,
                rating=4,
                comment="Review kedua.",
            )

            raise AssertionError(
                "Duplicate review was allowed"
            )

        except ValueError as e:
            if str(e) != "User has already reviewed this product":
                raise

            print("Duplicate review correctly rejected")

def test_user_cannot_delete_other_user_review():
    with SessionLocal() as session:
        service = ReviewService(session)

        # Ambil review milik User 1
        reviews = service.get_product_reviews(product_id=1)

        if not reviews:
            raise ValueError("No reviews found for product 1")

        review_id = reviews[0].id

        print(
            f"User 2 trying to delete User 1's Review {review_id}..."
        )

        try:
            service.delete_review(
                user_id=2,
                review_id=review_id,
            )

            raise AssertionError(
                "Authorization failed: User 2 can delete User 1's review"
            )

        except ValueError as e:
            if str(e) != "Review does not belong to this user":
                raise

            print("Authorization successful")
            print("User 2 was denied access to User 1's review")

def test_user_can_delete_own_review():
    with SessionLocal() as session:
        service = ReviewService(session)

        # Cari review milik User 1
        reviews = service.get_product_reviews(product_id=1)

        own_review = None

        for review in reviews:
            if review.user_id == 1:
                own_review = review
                break

        if own_review is None:
            raise ValueError("No review found for User 1")

        review_id = own_review.id

        print(f"User 1 deleting own Review {review_id}...")

        service.delete_review(
            user_id=1,
            review_id=review_id,
        )

        session.commit()

        print("Review deleted successfully")


if __name__ == "__main__":
    # test_create_review()
    test_get_product_rating()
    # test_get_product_reviews()
    # test_duplicate_review()
    # 
    # test_user_cannot_delete_other_user_review()
    # test_user_can_delete_own_review()