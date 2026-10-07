import requests
from fasthtml.common import *
from app.utils.formatter import format_rupiah

AI_SERVICE_URL = "http://127.0.0.1:8001"

def get_forecast(commodity: str):
    response = requests.get(
        f"{AI_SERVICE_URL}/api/forecast/{commodity}",
        timeout=60
    )

    response.raise_for_status()

    return response.json()

def get_commodities():
    response = requests.get(
        f"{AI_SERVICE_URL}/api/commodities",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

def ai_routes(rt):

    @rt("/ai/forecast")
    def forecast_home():
        commodities = get_commodities()

        return Titled(
            "AI Price Forecast",

            H1("AI Price Forecast"),

            A(
                "← Kembali ke Home",
                href="/"
            ),

            Br(),

            P("Pilih komoditas untuk melihat prediksi harga:"),

            Ul(
                *[
                    Li(
                        A(
                            commodity["name"],
                            href=f"/ai/forecast/{commodity['slug']}/view"
                        )
                    )
                    for commodity in commodities
                ]
            ),
        )

    @rt("/ai/forecast/{commodity}")
    def forecast(commodity: str):
        return get_forecast(commodity)

    @rt("/ai/forecast/{commodity}/view")
    def forecast_view(commodity: str):
        data = get_forecast(commodity)

        guard = data["auto_margin_guard"]

        return Titled(
            f"AI Forecast - {data['komoditas']}",

            H1("AI Price Forecast"),

            H2(data["komoditas"]),

            P(
                "Harga hari ini: ",
                Strong(format_rupiah(data["harga_riil_hari_ini"]))
            ),

            H3("Auto-Margin Guard"),

            P(
                Strong(guard["status"])
            ),

            P(guard["pesan"]),

            H3("Forecast 7 Hari"),

            Table(
                Thead(
                    Tr(
                        Th("Tanggal"),
                        Th("Prediksi Harga"),
                        Th("Batas Bawah"),
                        Th("Batas Atas"),
                    )
                ),
                Tbody(
                    *[
                        Tr(
                            Td(item["tanggal"]),
                            Td(format_rupiah(item["prediksi_harga"])),
                            Td(format_rupiah(item["batas_bawah"])),
                            Td(format_rupiah(item["batas_atas"])),
                        )
                        for item in data["forecast_7_hari"]
                    ]
                ),
            ),

            Br(),

            A(
                "← Kembali ke daftar komoditas",
                href="/ai/forecast"
            ),
        )