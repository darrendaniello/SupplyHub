from sqlalchemy.orm import Session

from app.models.user_address import UserAddress


class UserAddressRepository:

    def get_by_id(
        self,
        db: Session,
        address_id: int,
    ):
        return (
            db.query(UserAddress)
            .filter(UserAddress.id == address_id)
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(UserAddress)
            .filter(UserAddress.user_id == user_id)
            .order_by(
                UserAddress.is_default.desc(),
                UserAddress.created_at.desc(),
            )
            .all()
        )

    def get_default_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(UserAddress)
            .filter(
                UserAddress.user_id == user_id,
                UserAddress.is_default == True,
            )
            .first()
        )

    def create(
        self,
        db: Session,
        user_id: int,
        label: str,
        recipient_name: str,
        phone_number: str,
        address: str,
        is_default: bool = False,
    ):
        user_address = UserAddress(
            user_id=user_id,
            label=label,
            recipient_name=recipient_name,
            phone_number=phone_number,
            address=address,
            is_default=is_default,
        )

        db.add(user_address)
        db.flush()

        return user_address

    def update(
        self,
        db: Session,
        user_address: UserAddress,
        label: str,
        recipient_name: str,
        phone_number: str,
        address: str,
    ):
        user_address.label = label
        user_address.recipient_name = recipient_name
        user_address.phone_number = phone_number
        user_address.address = address

        db.flush()

        return user_address

    def delete(
        self,
        db: Session,
        user_address: UserAddress,
    ):
        db.delete(user_address)
        db.flush()