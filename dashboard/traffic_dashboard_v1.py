import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Konfigurasi Page
st.set_page_config(page_title="Smart City Traffic", layout="wide")

st.title('🏙️ Smart City Traffic Dashboard')

# Load Data untuk Visualisasi
@st.cache_data
def load_data():
    df = pd.read_csv('data/clean/traffic_smartcity_clean_v1.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

# Load Model untuk Prediksi
@st.cache_resource
def load_model():
    return joblib.load('models/traffic_model_v1.pkl')

try:
    df = load_data()
    model = load_model()

    # --- Bagian 1: Metrik Utama ---
    col1, col2 = st.columns(2)
    col1.metric("Avg Traffic", f"{round(df['traffic'].mean(), 2)} unit")
    col2.metric("Max Traffic", f"{df['traffic'].max()} unit")

    # --- Bagian 2: Visualisasi ---
    st.subheader("Traffic Trend")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['datetime'].tail(50), df['traffic'].tail(50), color='pink', marker='o')
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Volume Traffic")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # --- Bagian 3: Prediksi Real-time ---
    st.sidebar.header("Input Parameter Prediksi")
    with st.sidebar.form("prediction_form"):
        input_hour = st.slider("Jam (0-23)", 0, 23, 12)
        input_day = st.selectbox("Hari", options=list(range(7)), 
                                 format_func=lambda x: ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][x])
        input_lag = st.number_input("Traffic Sebelumnya (Lag1)", value=100)
        
        submit = st.form_submit_button("Prediksi Sekarang")

    if submit:
        features = [[input_hour, input_day, input_lag]]
        prediction = model.predict(features)
        st.sidebar.success(f"Hasil Prediksi: {round(prediction[0], 2)} unit kendaraan")

except Exception as e:
    st.error(f"Pastikan script cleaning dan modeling sudah dijalankan. Error: {e}")