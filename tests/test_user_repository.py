from app.database import SessionLocal
from app.repositories.user_repository import UserRepository

def test_get_user_by_id():
    with SessionLocal() as session:
        repo = UserRepository(session)

        user = repo.get_by_id(2)

        if user:
            print("\nUser found")
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Name: {user.full_name}")
            print(f"Role: {user.role}")
        else:
            print("\nUser not found")

def test_get_user_by_email():
    with SessionLocal() as session:
        repo = UserRepository(session)

        user = repo.get_by_email("buyer1@supplyhub.test")

        if user:
            print("\nUser found")
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Name: {user.full_name}")
            print(f"Role: {user.role}")
        else:
            print("\nUser not found")

def test_create_user():
    with SessionLocal() as session:
        repository = UserRepository(session)

        user = repository.create(
            email="test_user@supplyhub.com",
            password_hash="dummy_hash",
            full_name="Test User",
            role="BUYER",
        )

        session.commit()

        print("\nUser created.")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.full_name}")
        print(f"Role: {user.role}")

def test_update_user():
    with SessionLocal() as session:
        repository = UserRepository(session)

        user = repository.get_by_email(
            "test_user@supplyhub.com"
        )

        if not user:
            print("\nUser not found.")
            return

        print("\nBefore update:")
        print(f"Name: {user.full_name}")
        print(f"Role: {user.role}")

        updated_user = repository.update(
            user=user,
            full_name="Test User Updated",
        )

        session.commit()

        print("\nAfter update:")
        print(f"Name: {updated_user.full_name}")
        print(f"Role: {updated_user.role}")

def test_delete_user():
    with SessionLocal() as session:
        repository = UserRepository(session)

        user = repository.get_by_email(
            "test_user@supplyhub.com"
        )

        if not user:
            print("\nUser not found.")
            return

        print("\nBefore delete:")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.full_name}")

        repository.delete(user)

        session.commit()

        print("\nUser deleted.")

        deleted_user = repository.get_by_id(user.id)

        if deleted_user:
            print("User still exists.")
        else:
            print("User no longer exists.")

if __name__ == "__main__":
    # test_get_user_by_id()
    # test_get_user_by_email()
    # test_create_user()
    # test_update_user()
    test_delete_user()