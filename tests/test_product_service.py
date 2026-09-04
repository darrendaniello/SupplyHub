from app.database import SessionLocal
from app.services.product_service import ProductService


def test_get_available_products():
    with SessionLocal() as session:
        service = ProductService(session)

        products = service.get_available_products()

        print("\nAvailable products:")
        for product in products:
            print(
                product.id,
                product.name,
                product.selling_price,
            )


def test_search_products():
    with SessionLocal() as session:
        service = ProductService(session)

        products = service.search_products("beras")

        print("\nSearch results:")
        for product in products:
            print(
                product.id,
                product.name,
                product.selling_price,
            )


def test_get_products_by_category():
    with SessionLocal() as session:
        service = ProductService(session)

        products = service.get_products_by_category(1)

        print("\nProducts by category:")
        for product in products:
            print(
                product.id,
                product.name,
                product.selling_price,
            )


def test_get_products_by_business():
    with SessionLocal() as session:
        service = ProductService(session)

        products = service.get_products_by_business(1)

        print("\nProducts by business:")
        for product in products:
            print(
                product.id,
                product.name,
                product.selling_price,
            )


def test_get_product_detail():
    with SessionLocal() as session:
        service = ProductService(session)

        result = service.get_product_detail(1)

        product = result["product"]
        available_quantity = result["available_quantity"]

        print("\nProduct detail:")
        print("ID:", product.id)
        print("Name:", product.name)
        print("Price:", product.selling_price)
        print("Available quantity:", available_quantity)


if __name__ == "__main__":
    test_get_available_products()
    # test_search_products()
    # test_get_products_by_category()
    # test_get_products_by_business()
    # test_get_product_detail()