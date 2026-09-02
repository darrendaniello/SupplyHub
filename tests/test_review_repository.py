from app.database import SessionLocal
from app.repositories.review_repository import ReviewRepository
from app.models import Product

def test_get_reviews_by_product():
    session = SessionLocal()

    try:
        repository = ReviewRepository(session)

        reviews = repository.get_by_product(1)

        print(f"\nReviews for product 1: {len(reviews)}")

        for review in reviews:
            print(
                f"Review ID: {review.id} | "
                f"User ID: {review.user_id} | "
                f"Product ID: {review.product_id} | "
                f"Rating: {review.rating} | "
                f"Comment: {review.comment}"
            )

    finally:
        session.close()


def test_get_average_rating():
    session = SessionLocal()

    try:
        repository = ReviewRepository(session)

        average_rating = repository.get_average_rating(1)

        print(f"\nAverage rating for product 1: {average_rating}")

    finally:
        session.close()

def test_get_review_count():
    session = SessionLocal()

    try:
        repository = ReviewRepository(session)

        review_count = repository.get_review_count(1)

        print(f"\nReview count for product 1: {review_count}")

    finally:
        session.close()

def test_get_by_user_and_by_product():
    session = SessionLocal()

    try:
        repository = ReviewRepository(session)

        review = repository.get_by_user_and_by_product(
            user_id=1,
            product_id=4,
        )

        if review:
            print("\nReview found:")
            print(f"Review ID: {review.id}")
            print(f"User ID: {review.user_id}")
            print(f"Product ID: {review.product_id}")
            print(f"Rating: {review.rating}")
            print(f"Comment: {review.comment}")
        else:
            print("\nReview not found.")

    finally:
        session.close()

def test_create_review():
    session = SessionLocal()

    try:
        repository = ReviewRepository(session)

        review = repository.create(
            product_id=4,
            user_id=1,
            rating=5,
            comment="Produk sangat bagus.",
        )

        session.commit()

        print("\nReview created:")
        print(f"Review ID: {review.id}")
        print(f"User ID: {review.user_id}")
        print(f"Product ID: {review.product_id}")
        print(f"Rating: {review.rating}")
        print(f"Comment: {review.comment}")

    finally:
        session.close()

def test_delete_review():
    session = SessionLocal()

    try:
        repository = ReviewRepository(session)

        review = repository.get_by_user_and_by_product(
            user_id=1,
            product_id=4,
        )

        if not review:
            print("\nReview not found.")
            return

        print("\nReview before delete:")
        print(f"ID: {review.id}")
        print(f"Rating: {review.rating}")
        print(f"Comment: {review.comment}")

        repository.delete(review)

        session.commit()

        print("\nReview deleted successfully.")

    finally:
        session.close()

if __name__ == "__main__":
    # test_get_reviews_by_product()
    # test_get_average_rating()
    # test_get_review_count()
    test_get_by_user_and_by_product()
    # test_create_review()
    test_delete_review()