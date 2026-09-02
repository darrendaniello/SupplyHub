from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)

        return self.session.scalar(stmt)

    def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)

        return self.session.scalar(stmt)

    def create(
        self,
        email: str,
        password_hash: str,
        full_name: str,
        role: str = "BUYER",
    ):
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
        )

        self.session.add(user)
        self.session.flush()

        return user

    def update(
        self,
        user: User,
        email: str | None = None,
        password_hash: str | None = None,
        full_name: str | None = None,
        role: str | None = None,
    ):
        if email is not None:
            user.email = email

        if password_hash is not None:
            user.password_hash = password_hash

        if full_name is not None:
            user.full_name = full_name

        if role is not None:
            user.role = role

        self.session.flush()

        return user

    def delete(self, user: User):
        self.session.delete(user)
        self.session.flush()