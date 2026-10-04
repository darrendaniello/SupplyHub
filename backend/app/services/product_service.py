from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.inventory_repository import InventoryRepository

class ProductService:
    def __init__(self, session: Session):
        self.product_repository = ProductRepository(session)
        self.inventory_repository = InventoryRepository(session)

    def get_available_products(self):
        return self.product_repository.get_available_products()

    def search_products(self, keyword: str):
        if not keyword or not keyword.strip():
            return []

        return self.product_repository.search(keyword.strip())

    def filter_products(
        self,
        keyword: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        sort_by: str | None = None,
    ):
        if keyword is not None:
            keyword = keyword.strip()

        if keyword == "":
            keyword = None

        return self.product_repository.filter_products(
            keyword=keyword,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            sort_by=sort_by,
        )

    def get_products_by_category(self, category_id: int):
        return self.product_repository.get_by_category(category_id)

    def get_products_by_business(self, business_id: int):
        return self.product_repository.get_by_business(business_id)

    def get_product_detail(self, product_id: int):
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ValueError("Product not found.")

        inventory = self.inventory_repository.get_by_product(product_id)

        if inventory is None:
            available_quantity = None
        else:
            available_quantity = (
                inventory.stock_quantity - inventory.reserved_quantity
            )

        return {
            "product": product,
            "available_quantity": available_quantity
        }