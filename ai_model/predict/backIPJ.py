import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def tarik_data_historis(hari_kebelakang=90):
    print(f"=== MEMULAI BACKFILL DATA IPJ ({hari_kebelakang} HARI) ===")
    
    data_historis = []
    
    # Looping dari 90 hari yang lalu, maju terus sampai hari ini (0)
    for i in range(hari_kebelakang, -1, -1):
        target_tanggal = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
        
        url_base = "https://infopangan.jakarta.go.id/api2/v1/public/master-data/commodities?date="
        url_api = f"{url_base}{target_tanggal}"
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        
        try:
            print(f"[{target_tanggal}] Menarik data...")
            response = requests.get(url_api, headers=headers, timeout=15)
            response.raise_for_status()
            
            data_json = response.json()
            daftar_komoditas = data_json.get('data', {}).get('data', [])
            
            jumlah_valid = 0 
            
            for item in daftar_komoditas:
                komoditas = item.get('name', '').strip()
                harga_raw = item.get('newest_price', 0)
                
                try:
                    harga_bersih = int(float(harga_raw))
                except:
                    harga_bersih = 0
                    
                if harga_bersih > 0 and komoditas:
                    data_historis.append({
                        "tanggal": target_tanggal,
                        "komoditas": komoditas,
                        "lokasi": "Rata-rata DKI Jakarta",
                        "harga": harga_bersih
                    })
                    jumlah_valid += 1
            
            print(f"    -> Sukses: {jumlah_valid} komoditas tersimpan.")
            
        except Exception as e:
            print(f"    -> Gagal menarik data: {e}")
            
        time.sleep(1) 
        
    if data_historis:
        df_historis = pd.DataFrame(data_historis)
        nama_file = f"dataset_historis_ipj_{hari_kebelakang}_hari.csv"
        df_historis.to_csv(nama_file, index=False)
        print(f"\n✅ BACKFILL SELESAI! Total {len(df_historis)} baris data historis berhasil diamankan.")
        print(f"📁 Tersimpan di: {nama_file}")
    else:
        print("\n❌ Gagal mendapatkan data historis.")

if __name__ == "__main__":
    tarik_data_historis(90)