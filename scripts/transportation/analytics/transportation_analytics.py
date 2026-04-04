import pandas as pd

def load_data(path):
    """Membaca data Parquet dengan efisien menggunakan Pandas."""
    try:
        return pd.read_parquet(path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def preprocess(df):
    """Membersihkan dan memformat kolom timestamp."""
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Sort berdasarkan waktu untuk memastikan urutan data benar
        df = df.sort_values('timestamp')
    return df

def compute_metrics(df):
    """Menghitung metrik dasar untuk kartu informasi."""
    if df.empty:
        return 0, 0, "N/A"
    total_trips = len(df)
    total_fare = df['fare_amount'].sum()
    top_location = df['pickup_location'].mode()[0] if not df['pickup_location'].empty else "N/A"
    return total_trips, total_fare, top_location

def traffic_per_window(df):
    """
    KRUSIAL: Menggunakan Window Aggregation (1 menit) 
    untuk mengurangi jumlah titik data pada grafik agar tidak lag.
    """
    if df.empty:
        return pd.DataFrame()
    # Set index ke timestamp untuk resamping
    df_indexed = df.set_index('timestamp')
    windowed_df = df_indexed.resample('1min').size().reset_index(name='trip_count')
    return windowed_df

def detect_peak_hour(df):
    if df.empty: return "N/A"
    df['hour'] = df['timestamp'].dt.hour
    peak_hour = df.groupby('hour').size().idxmax()
    return f"{peak_hour}:00"

def fare_per_location(df):
    if df.empty: return pd.DataFrame()
    return df.groupby('pickup_location')['fare_amount'].mean().sort_values(ascending=False)

def vehicle_distribution(df):
    if df.empty: return pd.DataFrame()
    return df.groupby('vehicle_type').size()

def detect_anomaly(df):
    """Mendeteksi fare yang tidak wajar (> 500.000) atau lonjakan trafik."""
    if df.empty: return pd.DataFrame()
    anomalies = df[df['fare_amount'] > 500000]
    return anomalies