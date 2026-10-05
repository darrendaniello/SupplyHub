import requests
import pandas as pd
from datetime import datetime

def fetch_all_ipj_data():
    # 1. SETUP KONEKSI
    url_api = "https://infopangan.jakarta.go.id/api2/v1/public/master-data/commodities?date=" 
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    
    print(f"Menghubungi server Info Pangan Jakarta di: {url_api}...")
    
    try:
        response = requests.get(url_api, headers=headers, timeout=15)
        response.raise_for_status() 
        
        # 2. EKSTRAKSI JSON
        data_json = response.json()
        daftar_komoditas = data_json.get('data', {}).get('data', [])
        
        if not daftar_komoditas:
            print("Peringatan: Server merespons, tetapi daftar komoditas kosong.")
            return None
        
        print(f"Koneksi sukses! Ditemukan {len(daftar_komoditas)} data mentah. Memulai pembersihan...")
        
        # 3. PEMBERSIHAN DATA (TRANSFORM)
        data_bersih = []
        tanggal_hari_ini = datetime.today().strftime('%Y-%m-%d')
        
        for item in daftar_komoditas:
            komoditas = item.get('name', 'Tidak Diketahui').strip()
            # Karena ini data rata-rata seluruh kota, kita hardcode lokasinya
            pasar = "Rata-rata DKI Jakarta" 
            harga_raw = item.get('newest_price', 0)
            
            try:
                harga_bersih = int(float(harga_raw))
            except (ValueError, TypeError):
                harga_bersih = 0
                
            if harga_bersih > 0:
                data_bersih.append({
                    "tanggal": tanggal_hari_ini,
                    "komoditas": komoditas,
                    "lokasi": pasar,
                    "harga": harga_bersih
                })
                
        # 4. PENYIMPANAN DATA (LOAD)
        if data_bersih:
            df = pd.DataFrame(data_bersih)
            nama_file = f"dataset_ipj_{tanggal_hari_ini}.csv"
            df.to_csv(nama_file, index=False)
            
            print(f"\n✅ BERHASIL! {len(data_bersih)} baris data komoditas telah disimpan.")
            print(f"📁 Nama file: {nama_file}\n")
            print("--- Pratinjau 5 Data Pertama ---")
            print(df.head())
            return df
        else:
            print("Gagal: Tidak ada data valid yang bisa disimpan.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Terjadi kesalahan jaringan/HTTP: {e}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan sistem: {e}")

if __name__ == "__main__":
    fetch_all_ipj_data()