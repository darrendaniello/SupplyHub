from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity_sold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    sales_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    product = relationship(
        "Product",
        back_populates="sales_history",
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "sales_date",
            name="uq_product_sales_date",
        ),
        CheckConstraint(
            "quantity_sold >= 0",
            name="ck_sales_history_quantity_non_negative",
        )
    )