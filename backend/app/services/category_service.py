from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, session: Session):
        self.category_repository = CategoryRepository(session)

    def get_all_categories(self):
        return self.category_repository.get_all()