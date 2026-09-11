from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        stmt = select(Category).order_by(Category.name.asc())
        return self.session.scalars(stmt).all()