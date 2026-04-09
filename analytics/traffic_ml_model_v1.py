import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def train_model():
    # Load data bersih
    df = pd.read_csv('data/clean/traffic_smartcity_clean_v1.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])

    # 1. Feature Engineering
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.dayofweek
    df['lag1'] = df['traffic'].shift(1)
    
    # Hapus baris pertama karena lag1 akan bernilai NaN
    df = df.dropna()

    # Tentukan fitur (X) dan target (y)
    X = df[['hour', 'day', 'lag1']]
    y = df['traffic']

    # 2. Training Model
    print("Melatih model Random Forest...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 3. Export Model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/traffic_model_v1.pkl')
    print("Model berhasil disimpan di: models/traffic_model_v1.pkl")

if __name__ == "__main__":
    train_model()