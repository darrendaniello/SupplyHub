from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product

class ProductRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(
            Product.id == product_id
        )

        return self.session.scalar(stmt)

    def get_available_products(self) -> list[Product]:
        stmt = select(Product).where(
            Product.status == "AVAILABLE"
        )

        return self.session.scalars(stmt).all()

    def search(self, keyword: str) -> list[Product]:
        stmt = (
            select(Product)
            .where(
                Product.status == "AVAILABLE",
                Product.name.ilike(f"%{keyword}%"),
            )
            .order_by(Product.name)
        )

        return self.session.scalars(stmt).all()

    def get_by_category(self, category_id: int) -> list[Product]:
        stmt = (
            select(Product)
            .where(
                Product.category_id == category_id,
                Product.status == "AVAILABLE",
            )
            .order_by(Product.name)
        )

        return self.session.scalars(stmt).all()

    def get_by_business(self, business_id: int) -> list[Product]:
        stmt = (
            select(Product)
            .where(
                Product.business_id == business_id,
                Product.status == "AVAILABLE",
            )
            .order_by(Product.name)
        )

        return self.session.scalars(stmt).all()