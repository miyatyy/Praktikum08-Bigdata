import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Smart City Dashboard", layout="wide")

# Path ke Data Lake Parquet (Sesuaikan dengan output generator)
DATA_PATH = "data/output/transportation_data.parquet"

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_parquet(DATA_PATH)
    return pd.DataFrame()

st.title("🏙️ Real-Time Smart City Mobility")
st.markdown("Monitoring Trafik dan Transportasi Skala Besar")

# Placeholder untuk update otomatis
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        if not df.empty:
            # Preprocessing sederhana
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # 1. Metric Cards
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trips", len(df))
            col2.metric("Total Fare", f"Rp {df['fare_amount'].sum():,}")
            col3.metric("Top Location", df['pickup_location'].mode()[0])

            # 2. Real-Time Traffic Chart (Windowing 1 Menit)
            st.subheader("📈 Traffic Trend (Per Minute)")
            df_window = df.set_index('timestamp').resample('1min').size().reset_index(name='counts')
            fig_line = px.line(df_window, x='timestamp', y='counts')
            st.plotly_chart(fig_line, use_container_width=True)

            # 3. Distribution Charts
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🚗 Vehicle Distribution")
                fig_pie = px.pie(df, names='vehicle_type')
                st.plotly_chart(fig_pie)
            with c2:
                st.subheader("📍 Fare per Location")
                fare_loc = df.groupby('pickup_location')['fare_amount'].mean().reset_index()
                fig_bar = px.bar(fare_loc, x='pickup_location', y='fare_amount')
                st.plotly_chart(fig_bar)

            # 4. Recent Data Table
            st.subheader("📋 10 Data Terbaru")
            st.dataframe(df.tail(10), use_container_width=True)
        else:
            st.warning("Menunggu data dari generator... Pastikan trip_generator.py sedang berjalan.")

    time.sleep(5) # Refresh setiap 5 detik