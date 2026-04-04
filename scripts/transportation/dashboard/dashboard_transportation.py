import streamlit as st
import time
from analytics.transportation_analytics import (
    load_data, preprocess, compute_metrics, 
    traffic_per_window, fare_per_location, 
    vehicle_distribution, detect_anomaly
)

st.set_page_config(page_title="Smart City Traffic Dashboard", layout="wide")

# Konfigurasi
DATA_PATH = "data/output/transportation_data.parquet"
REFRESH_INTERVAL = 5

st.title("🏙️ Real-Time Mobility & Traffic Analytics")
st.markdown("Sistem Monitoring Transportasi Kota Cerdas")

# Placeholder untuk refresh otomatis
placeholder = st.empty()

while True:
    with placeholder.container():
        # 1. Load & Optimasi Data
        raw_df = load_data(DATA_PATH)
        df = preprocess(raw_df)
        
        # Optimasi Big Data: Ambil 1000 data terakhir untuk visualisasi detail
        sample_df = df.tail(1000)

        # 2. Metric Cards
        total_trips, total_fare, top_loc = compute_metrics(df)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Perjalanan", f"{total_trips:,}")
        col2.metric("Total Pendapatan", f"Rp {total_fare:,.0f}")
        col3.metric("Lokasi Teramai", top_loc)

        # 3. Real-Time Traffic Chart (Windowed)
        st.subheader("📈 Tren Trafik (Agregasi Per Menit)")
        windowed_data = traffic_per_window(df)
        st.line_chart(windowed_data.set_index('timestamp'))

        # 4. Spatial & Operational Charts
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📍 Rata-rata Fare per Lokasi")
            st.bar_chart(fare_per_location(sample_df))
        with c2:
            st.subheader("🚗 Distribusi Armada")
            st.write(vehicle_distribution(sample_df))

        # 5. Traffic Alerts & Anomalies
        anomalies = detect_anomaly(sample_df)
        if not anomalies.empty:
            st.warning(f"⚠️ Terdeteksi {len(anomalies)} transaksi tidak wajar!")
            st.dataframe(anomalies.tail(5))

        # 6. Real-Time Table (50 Terbaru)
        st.subheader("📋 Data Perjalanan Terbaru")
        st.table(sample_df.tail(50))

    time.sleep(REFRESH_INTERVAL)