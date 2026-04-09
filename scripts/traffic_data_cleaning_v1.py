import pandas as pd
import os

def clean_data():
    # Path input dan output
    input_path = 'data/raw/traffic_smartcity_v1.csv'
    output_path = 'data/clean/traffic_smartcity_clean_v1.csv'
    
    # Memastikan folder output tersedia
    os.makedirs('data/clean', exist_ok=True)

    print("Memulai proses cleaning...")
    df = pd.read_csv(input_path)

    # 1. Konversi datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # 2. Sorting dan dropna
    df = df.sort_values(by='datetime')
    df = df.dropna()

    # Simpan hasil
    df.to_csv(output_path, index=False)
    print(f"Data bersih berhasil disimpan di: {output_path}")

if __name__ == "__main__":
    clean_data()