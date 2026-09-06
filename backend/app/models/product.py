from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id"),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    minimum_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="AVAILABLE",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    business = relationship(
        "Business",
        back_populates="products",
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    inventory = relationship(
        "ProductInventory",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product",
    )

    favorites = relationship(
        "Favorite",
        back_populates="product",
    )

    sales_history = relationship(
        "SalesHistory",
        back_populates="product",
    )

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="product",
    )

    __table_args__ = (
        CheckConstraint(
            "minimum_order > 0",
            name="ck_product_minimum_order_positive",
        ),
        CheckConstraint(
            "cost_price >= 0",
            name="ck_product_cost_price_non_negative",
        ),
        CheckConstraint(
            "selling_price >= 0",
            name="ck_product_selling_price_non_negative",
        ),
    )