from fasthtml.common import *

from app.database import SessionLocal
from app.services.business_service import BusinessService


def business_routes(rt):

    @rt("/businesses/nearby")
    def nearby_businesses(
        latitude: str = "",
        longitude: str = "",
        radius: str = "10",
    ):
        session = SessionLocal()

        try:
            business_service = BusinessService(session)

            if not latitude or not longitude:
                return Titled(
                    "Nearby Businesses - SupplyHub",
                    H1("Nearby Businesses"),
                    P("Masukkan latitude dan longitude untuk mencari supplier terdekat."),
                    Form(
                        Label("Latitude"),
                        Input(
                            type="number",
                            name="latitude",
                            step="any",
                            required=True,
                        ),

                        Label("Longitude"),
                        Input(
                            type="number",
                            name="longitude",
                            step="any",
                            required=True,
                        ),

                        Label("Radius (km)"),
                        Input(
                            type="number",
                            name="radius",
                            value="10",
                            min="1",
                            step="any",
                        ),

                        Button("Find Nearby Businesses", type="submit"),

                        action="/businesses/nearby",
                        method="get",
                    ),
                    Br(),
                    A("← Kembali ke Home", href="/"),
                )

            parsed_latitude = float(latitude)
            parsed_longitude = float(longitude)
            parsed_radius = float(radius)

            results = business_service.get_nearby_businesses(
                latitude=parsed_latitude,
                longitude=parsed_longitude,
                radius_km=parsed_radius,
            )

            business_cards = []

            for business, distance_km in results:
                business_cards.append(
                    Div(
                        H3(business.business_name),
                        P(f"Type: {business.business_type}"),
                        P(f"Distance: {distance_km:.2f} km"),
                        P(
                            f"Address: "
                            f"{business.addresses[0].address_line}"
                            if business.addresses
                            else "Address unavailable"
                        ),
                        cls="business-card",
                    )
                )

            return Titled(
                "Nearby Businesses - SupplyHub",
                H1("Nearby Businesses"),
                P(
                    f"Showing businesses within "
                    f"{parsed_radius:.2f} km."
                ),
                Div(
                    *business_cards,
                    cls="business-list",
                ),
                Br(),
                A("← Search again", href="/businesses/nearby"),
                Br(),
                A("← Kembali ke Home", href="/"),
            )

        finally:
            session.close()