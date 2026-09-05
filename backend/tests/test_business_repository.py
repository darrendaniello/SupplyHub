from app.database import SessionLocal
from app.repositories.business_repository import BusinessRepository


def test_get_business_by_id():
    session = SessionLocal()

    try:
        repository = BusinessRepository(session)

        business = repository.get_by_id(1)

        if business:
            print("Business found:")
            print(f"ID: {business.id}")
            print(f"Name: {business.business_name}")
            print(f"Type: {business.business_type}")
            print(f"Description: {business.description}")
            print(f"Phone: {business.phone}")
        else:
            print("Business with ID 1 not found.")

    finally:
        session.close()

def test_get_all_businesses():
    session = SessionLocal()

    try:
        repository = BusinessRepository(session)

        businesses = repository.get_all()

        print(f"\nTotal businesses: {len(businesses)}")

        for business in businesses:
            print(
                f"{business.id} | "
                f"{business.business_name} | "
                f"{business.business_type}"
            )

    finally:
        session.close()

def test_get_businesses_by_type():
    session = SessionLocal()

    try:
        repository = BusinessRepository(session)

        businesses = repository.get_by_type("Supplier")

        print(f"\nSuppliers: {len(businesses)}")

        for business in businesses:
            print(
                f"{business.id} | "
                f"{business.business_name} | "
                f"{business.business_type}"
            )

    finally:
        session.close()

def test_search_businesses():
    session = SessionLocal()

    try:
        repository = BusinessRepository(session)

        businesses = repository.search("pangan")

        print(f"\nSearch result for 'pangan': {len(businesses)}")

        for business in businesses:
            print(
                f"{business.id} | "
                f"{business.business_name} | "
                f"{business.business_type}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    test_get_business_by_id()
    test_get_all_businesses()
    test_get_businesses_by_type()
    test_search_businesses()