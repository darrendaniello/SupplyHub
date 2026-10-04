from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Product, Review

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

    def filter_products(
        self,
        keyword: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        sort_by: str | None = None,
    ) -> list[Product]:

        average_rating = func.coalesce(
            func.avg(Review.rating),
            0
        )

        stmt = (
            select(Product)
            .outerjoin(
                Review,
                Review.product_id == Product.id,
            )
            .where(
                Product.status == "AVAILABLE"
            )
            .group_by(Product.id)
        )

        if keyword:
            stmt = stmt.where(
                Product.name.ilike(f"%{keyword}%")
            )

        if category_id:
            stmt = stmt.where(
                Product.category_id == category_id
            )

        if min_price is not None:
            stmt = stmt.where(
                Product.selling_price >= min_price
            )

        if max_price is not None:
            stmt = stmt.where(
                Product.selling_price <= max_price
            )

        if min_rating is not None:
            stmt = stmt.having(
                average_rating >= min_rating
            )

        if sort_by == "price_asc":
            stmt = stmt.order_by(
                Product.selling_price.asc()
            )

        elif sort_by == "price_desc":
            stmt = stmt.order_by(
                Product.selling_price.desc()
            )

        elif sort_by == "rating":
            stmt = stmt.order_by(
                average_rating.desc()
            )

        else:
            stmt = stmt.order_by(
                Product.name
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