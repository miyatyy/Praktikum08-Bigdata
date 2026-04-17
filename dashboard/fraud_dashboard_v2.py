import streamlit as st
import pandas as pd
import os
import time

# Set konfigurasi halaman agar lebih menarik
st.set_page_config(page_title="Fraud Detection Dashboard", page_icon="🚨", layout="wide")

st.title("🚨 Real-Time Fraud Detection Dashboard")
st.markdown("---")

# Definisikan path folder output dari Spark
path_output = "stream_data/realtime_output/"

def load_data():
    try:
        # 1. Cek apakah folder ada
        if not os.path.exists(path_output):
            return None, "Menunggu folder output dibuat oleh Spark..."
        
        # 2. Cek apakah ada file parquet di dalamnya
        files = [f for f in os.listdir(path_output) if f.endswith(".parquet")]
        if not files:
            return None, "Folder ada, tapi belum ada data transaksi yang masuk..."
        
        # 3. Baca data
        df = pd.read_parquet(path_output)
        
        # 4. Cek apakah data kosong
        if df.empty:
            return None, "File terbaca, tapi data masih kosong (sedang diproses)..."
            
        return df, None
    except Exception as e:
        return None, f"Sedang menyinkronkan data: {str(e)}"

# Load data menggunakan fungsi di atas
df, error_msg = load_data()

if df is not None:
    # --- BAGIAN METRIK ---
    col1, col2, col3 = st.columns(3)
    
    total_transaksi = len(df)
    total_fraud = len(df[df["status"] == "FRAUD"])
    persentase_fraud = (total_fraud / total_transaksi) * 100 if total_transaksi > 0 else 0

    col1.metric("Total Transaksi", f"{total_transaksi}")
    col2.metric("Total Fraud", f"{total_fraud}", delta_color="inverse")
    col3.metric("Rasio Fraud", f"{persentase_fraud:.2f}%")

    # --- BAGIAN GRAFIK & TABEL ---
    st.markdown("### Analisis Real-Time")
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.write("**Distribusi Status Transaksi**")
        st.bar_chart(df["status"].value_counts())

    with right_col:
        st.write("**10 Transaksi Terakhir**")
        # Menampilkan kolom penting saja untuk dashboard
        st.dataframe(df[["nama", "rekening_masked", "jumlah", "lokasi", "status"]].tail(10), use_container_width=True)

    # Auto-refresh sederhana
    time.sleep(3)
    st.rerun()

else:
    # Menampilkan pesan tunggu jika data belum siap
    st.info(error_msg)
    st.info("Pastikan Terminal Spark Streaming (Terminal 4) sudah berjalan.")
    time.sleep(5)
    st.rerun()