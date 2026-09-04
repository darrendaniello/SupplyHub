import bcrypt
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def register(
            self,
            email: str,
            password: str,
            full_name: str,
    ):
        if not email or not email.strip():
            raise ValueError("Email is required.")

        if not password:
            raise ValueError("Password is required.")

        if not full_name or not full_name.strip():
            raise ValueError("Full name is required.")

        email = email.strip().lower()
        full_name = full_name.strip()

        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("Email is already registered.")

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

        user = self.user_repository.create(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role="BUYER"
        )

        return user

    def login(
            self,
            email: str,
            password: str
    ):
        if not email or not email.strip():
            raise ValueError("Email is required.")

        if not password:
            raise ValueError("Password is required.")

        email = email.strip().lower()

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password.")

        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8")
        )

        if not password_valid:
            raise ValueError("Invalid email or password.")

        return user