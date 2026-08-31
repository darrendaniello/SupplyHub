from app.database import Base, engine

from app.models import (
    User,
    Business,
    Address,
    Category,
    Product,
    ProductInventory,
    Order,
    OrderItem,
    Favorite,
    SalesHistory,
    SearchLog,
)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")


if __name__ == "__main__":
    create_tables()