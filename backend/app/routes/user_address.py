from fasthtml.common import *

from app.database import SessionLocal
from app.services.user_address_service import UserAddressService

def user_address_routes(rt):

    @rt("/profile/addresses", methods=["GET"])
    def address_list(request):
        user_id = request.session.get("user_id")

        if not user_id:
            return RedirectResponse(
                "/login",
                status_code=303
            )

        session = SessionLocal()

        try:
            service = UserAddressService(session)

            addresses = service.get_user_addresses(user_id=user_id)

            return Titled(
                "My Addresses - SupplyHub",

                H1("My Addresses"),

                A(
                    "Add New Address",
                    href="/profile/addresses/new",
                ),

                Hr(),

                *[
                    Div(
                        H3(
                            address.label,
                            " ⭐ Default"
                            if address.is_default
                            else "",
                        ),

                        P(
                            Strong(address.recipient_name)
                        ),

                        P(
                            address.phone_number
                        ),

                        P(
                            address.address
                        ),

                        (
                            Form(
                                Button(
                                    "Set as Default",
                                    type="submit",
                                ),
                                action=(
                                    f"/profile/addresses/"
                                    f"{address.id}/default"
                                ),
                                method="post",
                            )
                        )
                        if not address.is_default
                        else None,

                        Form(
                            Button(
                                "Delete",
                                type="submit",
                            ),
                            action=(
                                f"/profile/addresses/"
                                f"{address.id}/delete"
                            ),
                            method="post",
                        ),

                        Hr(),
                    )
                    for address in addresses
                ],
            )

        finally:
            session.close()

    @rt("/profile/addresses/{address_id}/default", methods=["POST"])
    def set_default_address(
        request,
        address_id: int
    ):
        user_id = request.session.get("user_id")

        if not user_id:
            return RedirectResponse(
                "/login",
                status_code=303
            )

        session = SessionLocal()

        try:
            service = UserAddressService(session)

            service.set_default_address(
                user_id=user_id,
                address_id=address_id
            )

            session.commit()

            return RedirectResponse(
                "/profile/addresses",
                status_code=303
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Address Error - SupplyHub",
                H1("Address Error"),
                P(str(error)),
                A(
                    "Back to addresses",
                    href="/profile/addresses",
                ),
            )

        except Exception as error:
            session.rollback()

            print(
                "SET DEFAULT ADDRESS ERROR:",
                repr(error),
            )

            return Titled(
                "Address Error - SupplyHub",
                H1("Address Error"),
                P("An unexpected error occurred."),
                A(
                    "Back to addresses",
                    href="/profile/addresses",
                ),
            )

        finally:
            session.close()

    @rt("/profile/addresses/{address_id}/delete", methods=["POST"])
    def delete_address(
        request,
        address_id: int,
    ):
        user_id = request.session.get("user_id")

        if not user_id:
            return RedirectResponse(
                "/login",
                status_code=303
            )

        session = SessionLocal()

        try:
            service = UserAddressService(session)

            service.delete_address(
                user_id=user_id,
                address_id=address_id
            )

            session.commit()

            return RedirectResponse(
                "/profile/addresses",
                status_code=303
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Address Error - SupplyHub",
                H1("Address Error"),
                P(str(error)),
                A(
                    "Back to addresses",
                    href="/profile/addresses",
                ),
            )

        except Exception as error:
            session.rollback()

            print("DELETE ADDRESS ERROR:", repr(error))

            return Titled(
                "Address Error - SupplyHub",
                H1("Address Error"),
                P("An unexpected error occurred."),
                A(
                    "Back to addresses",
                    href="/profile/addresses",
                ),
            )

        finally:
            session.close()

    @rt("/profile/addresses/new", methods=["GET"])
    def new_address_page(request):

        user_id = request.session.get("user_id")

        if not user_id:
            return RedirectResponse(
                "/login",
                status_code=303,
            )

        return Titled(
            "Add Address - SupplyHub",

            H1("Add New Address"),

            Form(
                Label("Label"),
                Input(
                    name="label",
                    placeholder="Home, Office, etc.",
                    required=True,
                ),

                Label("Recipient Name"),
                Input(
                    name="recipient_name",
                    placeholder="Recipient name",
                    required=True,
                ),

                Label("Phone Number"),
                Input(
                    name="phone_number",
                    type="tel",
                    placeholder="Phone number",
                    required=True,
                ),

                Label("Address"),
                Textarea(
                    name="address",
                    placeholder="Full address",
                    required=True,
                ),

                Label(
                    Input(
                        type="checkbox",
                        name="is_default",
                        value="true",
                    ),
                    " Set as default address",
                ),

                Br(),

                Button(
                    "Save Address",
                    type="submit",
                ),

                A(
                    "Cancel",
                    href="/profile/addresses",
                ),

                action="/profile/addresses/new",
                method="post",
            ),
        )

    @rt("/profile/addresses/new", methods=["POST"])
    def create_address(
        request,
        label: str,
        recipient_name: str,
        phone_number: str,
        address: str,
        is_default: str = "",
    ):
        user_id = request.session.get("user_id")

        if not user_id:
            return RedirectResponse(
                "/login",
                status_code=303,
            )

        session = SessionLocal()

        try:
            service = UserAddressService(session)

            new_address = service.create_address(
                user_id=user_id,
                label=label,
                recipient_name=recipient_name,
                phone_number=phone_number,
                address=address,
                is_default=is_default == "true",
            )

            session.commit()

            return RedirectResponse(
                "/profile/addresses",
                status_code=303,
            )

        except ValueError as error:
            session.rollback()

            print(
                "CREATE ADDRESS VALIDATION ERROR:",
                repr(error),
            )

            return Titled(
                "Address Error - SupplyHub",
                H1("Address Error"),
                P(str(error)),
                A(
                    "Back to addresses",
                    href="/profile/addresses",
                ),
            )

        except Exception as error:
            session.rollback()

            print(
                "CREATE ADDRESS ERROR:",
                repr(error),
            )

            return Titled(
                "Address Error - SupplyHub",
                H1("Address Error"),
                P(str(error)),
                A(
                    "Back to addresses",
                    href="/profile/addresses",
                ),
            )

        finally:
            session.close()