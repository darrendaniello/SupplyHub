import pandas as pd
from prophet import Prophet
import logging

# Menyembunyikan log internal Prophet agar terminal tetap bersih
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

def run_real_forecasting():
    print("=== MENGINISIASI AI FORECASTING DENGAN DATA HISTORIS ASLI ===")
    
    # 1. BACA DATA HISTORIS DARI CSV RAKSASA
    nama_file_csv = "dataset_historis_ipj_90_hari.csv" 
    try:
        df_historis = pd.read_csv(nama_file_csv)
    except FileNotFoundError:
        print(f"Error: File {nama_file_csv} tidak ditemukan.")
        return

    # 2. PILIH KOMODITAS UNTUK DIUJI
    target_komoditas = [
        "Minyak Goreng (Kuning/Curah)",
        "Telur Ayam Ras",
        "Beras IR. I (IR 64)",
        "Gula Pasir"
    ]

    for komoditas in target_komoditas:
        df_barang = df_historis[df_historis['komoditas'] == komoditas].copy()
        
        if df_barang.empty:
            print(f"[-] {komoditas} tidak ditemukan di dataset historis.")
            continue
            
        # 3. PERSIAPAN DATA UNTUK PROPHET 
        # Prophet hanya mau menerima tabel dengan kolom bernama 'ds' (tanggal) dan 'y' (harga)
        df_prophet = df_barang[['tanggal', 'harga']].rename(columns={'tanggal': 'ds', 'harga': 'y'})
        df_prophet = df_prophet.sort_values(by='ds')
        
        # harga asli hari ini untuk perbandingan
        harga_hari_ini = df_prophet.iloc[-1]['y']
        print(f"\nMemproses: {komoditas} | Total Sejarah: {len(df_prophet)} hari")
        print(f"    -> Harga Asli Hari Ini  : Rp {harga_hari_ini:,.0f}")
        
        # 4. TRAINING
        model = Prophet(yearly_seasonality=False, daily_seasonality=False)
        model.fit(df_prophet)
        
        # 5. PREDIKSI MASA DEPAN (7 Hari ke depan)
        future = model.make_future_dataframe(periods=7)
        forecast = model.predict(future)
        besok = forecast.iloc[-7]
        tren = "NAIK 📈" if besok['yhat'] > harga_hari_ini else "TURUN 📉"
        
        print(f"    -> Prediksi Harga Besok : Rp {besok['yhat']:,.0f} ({tren})")
        print(f"    -> Batas Toleransi      : Rp {besok['yhat_lower']:,.0f} s/d Rp {besok['yhat_upper']:,.0f}")
        
    print("\n=== PROSES FORECASTING SELESAI ===")

if __name__ == "__main__":
    run_real_forecasting()