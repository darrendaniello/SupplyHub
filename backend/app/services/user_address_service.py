from app.models.user_address import UserAddress
from app.repositories.user_address_repository import UserAddressRepository


class UserAddressService:

    def __init__(self, session):
        self.session = session
        self.repository = UserAddressRepository()

    def get_user_addresses(self, user_id: int):
        return self.repository.get_by_user(
            self.session,
            user_id,
        )

    def get_address(
        self,
        user_id: int,
        address_id: int,
    ):
        address = self.repository.get_by_id(
            self.session,
            address_id,
        )

        if not address:
            raise ValueError("Address not found")

        if address.user_id != user_id:
            raise ValueError(
                "You do not have permission to access this address"
            )

        return address

    def create_address(
        self,
        user_id: int,
        label: str,
        recipient_name: str,
        phone_number: str,
        address: str,
        is_default: bool = False,
    ):
        existing_addresses = self.repository.get_by_user(
            self.session,
            user_id,
        )

        # Alamat pertama otomatis menjadi default
        if not existing_addresses:
            is_default = True

        if is_default:
            self._clear_default_addresses(user_id)

        return self.repository.create(
            db=self.session,
            user_id=user_id,
            label=label,
            recipient_name=recipient_name,
            phone_number=phone_number,
            address=address,
            is_default=is_default,
        )

    def update_address(
        self,
        user_id: int,
        address_id: int,
        label: str,
        recipient_name: str,
        phone_number: str,
        address: str,
        is_default: bool = False,
    ):
        user_address = self.get_address(
            user_id,
            address_id,
        )

        if is_default:
            self._clear_default_addresses(user_id)
            user_address.is_default = True

        return self.repository.update(
            db=self.session,
            user_address=user_address,
            label=label,
            recipient_name=recipient_name,
            phone_number=phone_number,
            address=address,
        )

    def delete_address(
        self,
        user_id: int,
        address_id: int,
    ):
        user_address = self.get_address(
            user_id,
            address_id,
        )

        was_default = user_address.is_default

        self.repository.delete(
            self.session,
            user_address,
        )

        if was_default:
            remaining_addresses = self.repository.get_by_user(
                self.session,
                user_id,
            )

            if remaining_addresses:
                remaining_addresses[0].is_default = True

        return user_address

    def set_default_address(
        self,
        user_id: int,
        address_id: int,
    ):
        user_address = self.get_address(
            user_id,
            address_id,
        )

        self._clear_default_addresses(user_id)

        user_address.is_default = True

        self.session.flush()

        return user_address

    def _clear_default_addresses(
        self,
        user_id: int,
    ):
        addresses = self.repository.get_by_user(
            self.session,
            user_id,
        )

        for address in addresses:
            address.is_default = False