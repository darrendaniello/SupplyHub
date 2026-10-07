from sqlalchemy.orm import Session

from app.repositories.business_repository import BusinessRepository


class BusinessService:
    def __init__(self, session: Session):
        self.repository = BusinessRepository(session)

    def get_nearby_businesses(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 10,
    ):
        return self.repository.get_nearby_businesses(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
        )