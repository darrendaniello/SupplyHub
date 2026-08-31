from fastapi import FastAPI, HTTPException
import pandas as pd
from prophet import Prophet
import logging
import re
import requests
from sqlalchemy import create_engine, text 

logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

# =====================================================================
# 1. KONEKSI DATABASE POSTGIS
# =====================================================================
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_4YFyixLJSz2H@ep-small-rain-az8ptns1-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

try:
    engine = create_engine(DATABASE_URL)
    print("✅ Berhasil siap terhubung ke Database Neon PostGIS milik Darren!")
except Exception as e:
    print(f"⚠️ Gagal terhubung ke Database: {e}")
    engine = None

# =====================================================================
# 2. MEMBANGUN KAMUS KOMODITAS OTOMATIS DARI DATABASE IPJ
# =====================================================================
try:
    df_master = pd.read_csv("../predict/dataset_historis_ipj_90_hari.csv")
    semua_komoditas_ipj = df_master['komoditas'].str.lower().unique()
    
    kamus_dinamis = set()
    for item in semua_komoditas_ipj:
        item_bersih = re.sub(r'[^\w\s]', '', item)
        kata_pertama = item_bersih.split()[0]
        kamus_dinamis.add(kata_pertama)
        
    KAMUS_KOMODITAS = list(kamus_dinamis)
    print(f"✅ Sukses memuat {len(KAMUS_KOMODITAS)} kata kunci komoditas dari IPJ.")
except FileNotFoundError:
    print("⚠️ Database IPJ tidak ditemukan! Menggunakan kamus darurat.")
    KAMUS_KOMODITAS = ["beras", "minyak", "telur", "gula", "daging", "cabai", "bawang"]

# Inisialisasi Aplikasi FastAPI
app = FastAPI(title="SupplyHub API Backend")

@app.get("/")
def read_root():
    return {"message": "Server Backend SupplyHub Aktif!"}

# =====================================================================
# 3. ENDPOINT UTAMA: FORECASTING & AUTO-MARGIN Guard
# =====================================================================
@app.get("/api/forecast/{nama_komoditas}")
def get_forecast(nama_komoditas: str):
    try:
        df_historis = pd.read_csv("../predict/dataset_historis_ipj_90_hari.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Database historis tidak ditemukan.")

    df_barang = df_historis[df_historis['komoditas'].str.contains(nama_komoditas, case=False)]
    
    if df_barang.empty:
        raise HTTPException(status_code=404, detail=f"Komoditas '{nama_komoditas}' tidak ditemukan di pasar.")

    nama_lengkap_komoditas = df_barang.iloc[0]['komoditas']
    df_prophet = df_barang[['tanggal', 'harga']].rename(columns={'tanggal': 'ds', 'harga': 'y'}).sort_values(by='ds')
    harga_hari_ini = int(df_prophet.iloc[-1]['y'])

    model = Prophet(yearly_seasonality=False, daily_seasonality=False)
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    prediksi_7_hari = forecast.tail(7)

    daftar_prediksi = []
    for index, row in prediksi_7_hari.iterrows():
        daftar_prediksi.append({
            "tanggal": row['ds'].strftime('%Y-%m-%d'),
            "prediksi_harga": int(row['yhat']),
            "batas_bawah": int(row['yhat_lower']),
            "batas_atas": int(row['yhat_upper'])
        })

    harga_besok = daftar_prediksi[0]['prediksi_harga']
    selisih_harga = harga_besok - harga_hari_ini
    
    status_margin = "AMAN"
    pesan_notifikasi = "Harga bahan baku stabil. Margin keuntungan UMKM Anda aman."
    
    if selisih_harga > 500:
        status_margin = "BAHAYA"
        pesan_notifikasi = f"⚠️ PERINGATAN AUTO-MARGIN! Harga diprediksi melonjak naik Rp {selisih_harga} besok. Disarankan untuk menambah stok hari ini!"
    elif selisih_harga < 0:
        status_margin = "TURUN"
        pesan_notifikasi = f"Kabar baik, harga diprediksi turun Rp {abs(selisih_harga)} besok. Anda bisa menunda restock."

    return {
        "komoditas": nama_lengkap_komoditas,
        "harga_riil_hari_ini": harga_hari_ini,
        "auto_margin_guard": {
            "status": status_margin,
            "pesan": pesan_notifikasi
        },
        "forecast_7_hari": daftar_prediksi
    }

# =====================================================================
# 4. SUPER ENDPOINT: NLP & GEOSPATIAL ORCHESTRATION
# =====================================================================
@app.get("/api/smart-search")
def nlp_smart_search(query: str):
    teks_bersih = query.lower()
    teks_bersih_tanpa_simbol = re.sub(r'[^\w\s]', '', teks_bersih)
    
    komoditas_ditemukan = None
    lokasi_teks = None
    koordinat_peta = None
    
    # NLP: Mencari Komoditas
    for barang in KAMUS_KOMODITAS:
        if barang in teks_bersih_tanpa_simbol:
            komoditas_ditemukan = barang
            break
            
    # NLP: Mencari Lokasi
    pola_lokasi = re.search(r'\b(?:di sekitar|di daerah|di|daerah|sekitar)\s+([a-z]+(?:\s+[a-z]+)*)', teks_bersih_tanpa_simbol)
    
    if pola_lokasi:
        lokasi_mentah = pola_lokasi.group(1).strip()
        lokasi_teks = " ".join(lokasi_mentah.split()[:2])

        # Integrasi Satelit OpenStreetMap
        try:
            url_osm = "https://nominatim.openstreetmap.org/search"
            params = {"q": f"{lokasi_teks}, Jakarta, Indonesia", "format": "json", "limit": 1}
            headers = {"User-Agent": "SupplyHub_App_MVP"}
            response = requests.get(url_osm, params=params, headers=headers)
            data_osm = response.json()
            
            if len(data_osm) > 0:
                koordinat_peta = {
                    "latitude": float(data_osm[0]["lat"]),
                    "longitude": float(data_osm[0]["lon"]),
                    "nama_lengkap_lokasi": data_osm[0]["display_name"]
                }
        except Exception:
            pass

    # --- GEOSPATIAL CLUSTERING: Mencari Toko Terdekat di PostGIS ---
    rekomendasi_toko = []
    if koordinat_peta and engine and komoditas_ditemukan:
        try:
            lat = koordinat_peta["latitude"]
            lon = koordinat_peta["longitude"]
            
            # JOIN 3 Tabel (Toko, Alamat, dan Produk) & Filter Komoditas
            query_spasial = text("""
                SELECT 
                    b.business_name, 
                    a.address_line,
                    p.name AS product_name,
                    p.selling_price,
                    ST_DistanceSphere(a.geom, ST_MakePoint(:lon, :lat)) as jarak_meter
                FROM businesses b
                JOIN addresses a ON b.id = a.business_id
                JOIN products p ON b.id = p.business_id
                WHERE p.name ILIKE :komoditas AND p.status = 'AVAILABLE'
                ORDER BY a.geom <-> ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                LIMIT 3;
            """)
            
            with engine.connect() as conn:
                hasil = conn.execute(query_spasial, {
                    "lon": lon, 
                    "lat": lat,
                    "komoditas": f"%{komoditas_ditemukan}%"
                })
                
                for baris in hasil:
                    rekomendasi_toko.append({
                        "nama_toko": baris[0],
                        "alamat": baris[1],
                        "nama_produk": baris[2],
                        "harga": float(baris[3]), 
                        "jarak_km": round(baris[4] / 1000, 2)
                    })
        except Exception as e:
            print(f"⚠️ Error pencarian spasial PostGIS: {e}")
            
    # --- ORKESTRASI AI ---
    hasil_forecasting = None
    if komoditas_ditemukan:
        try:
            hasil_forecasting = get_forecast(komoditas_ditemukan)
        except HTTPException:
            pass

    # Evaluasi Status Response
    if komoditas_ditemukan and koordinat_peta:
        pesan = "Sukses! Komoditas dan Titik Koordinat Satelit berhasil dideteksi."
    elif komoditas_ditemukan and lokasi_teks:
        pesan = f"Komoditas ketemu, lokasi '{lokasi_teks}' terdeteksi dari teks tapi satelit tidak bisa menemukannya."
    elif komoditas_ditemukan:
        pesan = "Komoditas ditemukan, tapi lokasi tidak spesifik (Gunakan radius default)."
    else:
        pesan = "Tidak mengerti. Tolong sebutkan nama bahan baku yang dicari."

    return {
        "query_asli": query,
        "status": pesan,
        "entitas": {
            "komoditas": komoditas_ditemukan,
            "lokasi_teks": lokasi_teks,
            "koordinat_peta": koordinat_peta
        },
        "rekomendasi_toko_terdekat": rekomendasi_toko,
        "data_ai_prophet": hasil_forecasting
    }