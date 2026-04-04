import pandas as pd
import time
import random
import os
from datetime import datetime

# Pastikan folder output ada
OUTPUT_PATH = "data/output/transportation_data.parquet"
os.makedirs("data/output", exist_ok=True)

vehicles = ['Taxi-001', 'Bus-010', 'Ojek-05', 'Taxi-002', 'Bus-012']
locations = ['Sudirman', 'Thamrin', 'Kuningan', 'Blok M', 'Senen']

print("🚀 Generator dimulai... Menulis data ke Parquet Data Lake...")

try:
    while True:
        # Buat 1 data dummy
        new_data = {
            "timestamp": [datetime.now()],
            "vehicle_id": [random.choice(vehicles)],
            "vehicle_type": [random.choice(['Car', 'Motorcycle', 'Bus'])],
            "pickup_location": [random.choice(locations)],
            "fare_amount": [random.randint(10000, 150000)]
        }
        df_new = pd.DataFrame(new_data)

        # Simpan/Append ke file Parquet
        if not os.path.isfile(OUTPUT_PATH):
            df_new.to_parquet(OUTPUT_PATH, index=False)
        else:
            # Baca data lama dan gabungkan (Simulasi Data Lake sederhana)
            df_old = pd.read_parquet(OUTPUT_PATH)
            df_final = pd.concat([df_old, df_new], ignore_index=True)
            # Batasi agar file tidak terlalu raksasa di lokal (opsional)
            df_final.tail(5000).to_parquet(OUTPUT_PATH, index=False)

        print(f"Data ditambahkan: {new_data['timestamp'][0]} - {new_data['vehicle_id'][0]}")
        time.sleep(2) # Kirim data setiap 2 detik
except KeyboardInterrupt:
    print("\nGenerator dihentikan.")