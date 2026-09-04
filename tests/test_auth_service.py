from app.database import SessionLocal
from app.services.auth_service import AuthService


def test_register():
    with SessionLocal() as session:
        service = AuthService(session)

        user = service.register(
            email="auth_test@supplyhub.com",
            password="Password123!",
            full_name="Auth Test User",
        )

        session.commit()

        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.full_name}")
        print(f"Role: {user.role}")
        print(f"Password Hash: {user.password_hash}")


def test_login():
    with SessionLocal() as session:
        service = AuthService(session)

        user = service.login(
            email="auth_test@supplyhub.com",
            password="Password123!",
        )

        print(f"Logged in user: {user.email}")
        print(f"User ID: {user.id}")
        print(f"Role: {user.role}")


if __name__ == "__main__":
    # test_register()
    test_login()