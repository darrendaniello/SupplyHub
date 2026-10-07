from sqlalchemy import func, select
from sqlalchemy.orm import Session
from geoalchemy2 import Geography

from app.models import Business, Address


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

    def get_nearby_businesses(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 10,
    ):
        user_point = func.ST_SetSRID(
            func.ST_MakePoint(longitude, latitude),
            4326,
        )

        distance = func.ST_Distance(
            Address.geom.cast(Geography),
            user_point.cast(Geography),
        )

        stmt = (
            select(
                Business,
                (distance / 1000).label("distance_km"),
            )
            .join(
                Address,
                Address.business_id == Business.id,
            )
            .where(
                func.ST_DWithin(
                    Address.geom.cast(Geography),
                    user_point.cast(Geography),
                    radius_km * 1000,
                )
            )
            .order_by(distance)
        )

        return self.session.execute(stmt).all()