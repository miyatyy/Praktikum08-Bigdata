import pandas as pd
import os

def load_data(path):
    if os.path.exists(path):
        return pd.read_parquet(path)
    return pd.DataFrame()

def preprocess(df):
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    return df

def compute_metrics(df):
    if df.empty: return 0, 0, "N/A"
    total_trips = len(df)
    total_fare = df['fare_amount'].sum()
    top_location = df['pickup_location'].mode()[0] if not df['pickup_location'].empty else "N/A"
    return total_trips, total_fare, top_location

def traffic_per_window(df):
    if df.empty: return pd.DataFrame()
    df_indexed = df.set_index('timestamp')
    return df_indexed.resample('1min').size().reset_index(name='trip_count')

def fare_per_location(df):
    if df.empty: return pd.DataFrame()
    return df.groupby('pickup_location')['fare_amount'].mean()

def vehicle_distribution(df):
    if df.empty: return pd.DataFrame()
    return df.groupby('vehicle_type').size()

def detect_anomaly(df):
    if df.empty: return pd.DataFrame()
    return df[df['fare_amount'] > 120000] # Contoh ambang batas anomali