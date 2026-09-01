from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Business


class BusinessRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, business_id: int) -> Business | None:
        stmt = select(Business).where(
            Business.id == business_id
        )

        return self.session.scalar(stmt)

    def get_all(self) -> list[Business]:
        stmt = (
            select(Business)
            .order_by(Business.business_name)
        )

        return self.session.scalars(stmt).all()


    def get_by_type(self, business_type: str) -> list[Business]:
        stmt = (
            select(Business).where(
                Business.business_type == business_type
            ).order_by(
                Business.business_name
            )
        )

        return self.session.scalars(stmt).all()

    def search(self, keyword: str) -> list[Business]:
        stmt = (
            select(Business).where(
                Business.business_name.ilike(f"%{keyword}%")
            ).order_by(
                Business.business_name
            )
        )

        return self.session.scalars(stmt).all()