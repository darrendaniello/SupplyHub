from app.database import SessionLocal
from app.repositories.product_repository import ProductRepository


def test_get_product_by_id():
    session = SessionLocal()

    try:
        repository = ProductRepository(session)

        product = repository.get_by_id(1)

        if product:
            print("Product found:")
            print(f"ID: {product.id}")
            print(f"Name: {product.name}")
            print(f"Business ID: {product.business_id}")
            print(f"Category ID: {product.category_id}")
            print(f"Selling Price: {product.selling_price}")
        else:
            print("Product with ID 1 not found.")

    finally:
        session.close()

def test_get_available_products():
    session = SessionLocal()

    try:
        repository = ProductRepository(session)

        products = repository.get_available_products()

        print(f"\nAvailable products: {len(products)}")

        for product in products:
            print(
                f"{product.id} | "
                f"{product.name} | "
                f"{product.status}"
            )

    finally:
        session.close()

def test_search_products():
    session = SessionLocal()

    try:
        repository = ProductRepository(session)

        products = repository.search("Bawang")

        print(f"\nSearch results for 'Bawang': {len(products)}")

        for product in products:
            print(
                f"{product.id} | "
                f"{product.name} | "
                f"{product.selling_price}"
            )

    finally:
        session.close()

def test_get_products_by_category():
    session = SessionLocal()

    try:
        repository = ProductRepository(session)

        products = repository.get_by_category(1)

        print(f"\nProducts in category 1: {len(products)}")

        for product in products:
            print(
                f"{product.id} | "
                f"{product.name} | "
                f"Category: {product.category_id} | "
                f"Status: {product.status}"
            )

    finally:
        session.close()

def test_get_products_by_business():
    session = SessionLocal()

    try:
        repository = ProductRepository(session)

        products = repository.get_by_business(1)

        print(f"\nProducts from business 1: {len(products)}")

        for product in products:
            print(
                f"{product.id} | "
                f"{product.name} | "
                f"Business: {product.business_id} | "
                f"Status: {product.status}"
            )

    finally:
        session.close()

if __name__ == "__main__":
    # test_get_product_by_id()
    # test_get_available_products()
    # test_search_products()
    test_get_products_by_category()
    test_get_products_by_business()
