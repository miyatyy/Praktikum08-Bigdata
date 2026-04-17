# 🚨 Real-Time Fraud Detection System (Big Data)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.5.1-orange?style=for-the-badge&logo=apachespark)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-3.5.1-black?style=for-the-badge&logo=apachekafka)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)

### 📌 Ringkasan Proyek
Proyek ini dikembangkan untuk memenuhi tugas **Praktikum 08: Keamanan dan Privasi Big Data**. Fokus utama proyek ini adalah membangun *pipeline* data *real-time* yang mampu mendeteksi transaksi mencurigakan (*fraud*) pada sistem perbankan sekaligus menerapkan protokol keamanan data.

### 🛡️ Fitur Keamanan
Sesuai dengan prinsip privasi data, sistem ini menerapkan:
1. **Data Masking**: Nomor rekening nasabah disembunyikan secara dinamis, hanya menampilkan 2 digit terakhir untuk melindungi identitas.
2. **Data Encryption**: Nominal transaksi dienkripsi menggunakan algoritma **Base64** sebelum disimpan ke penyimpanan permanen (Parquet).
3. **Real-Time Detection**: Logika deteksi otomatis untuk transaksi di atas 50jt atau lokasi mencurigakan (Luar Negeri).

### 🏗️ Arsitektur Pipeline
Sistem bekerja dengan urutan sebagai berikut:
1. **Producer**: Mensimulasikan data transaksi nasabah ke Kafka Topic.
2. **Kafka Broker**: Mengelola antrean data *streaming*.
3. **Spark Streaming**: Melakukan transformasi, keamanan (masking/enkripsi), dan analisis fraud secara *real-time*.
4. **Parquet Storage**: Menyimpan hasil olahan data yang aman ke folder `realtime_output`.
5. **Dashboard**: Visualisasi data interaktif bagi tim keamanan bank.

### 🚀 Cara Menjalankan
1. **Infrastruktur**: Jalankan Zookeeper dan Kafka Server.
2. **Producer**: `python scripts/kafka_producer_bank.py`
3. **Processor**: `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 scripts/spark_streaming_fraud_v2.py`
4. **Visualisasi**: `streamlit run dashboard/fraud_dashboard_v2.py`

---
**👤 Author**
* **Nama**: Nurmiyaty
* **Mata Kuliah**: Big Data Technology
* **Dosen**: Muhayat, M.IT
