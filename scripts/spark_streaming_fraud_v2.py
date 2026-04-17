from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Fraud Detection").getOrCreate()

# Ingest data dari Kafka
df_kafka = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bank_topic") \
    .load()

schema = StructType([
    StructField("nama", StringType()),
    StructField("rekening", StringType()),
    StructField("jumlah", IntegerType()),
    StructField("lokasi", StringType())
])

df = df_kafka.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# 1. Masking: Sembunyikan no rekening kecuali 2 digit terakhir [cite: 157, 158]
df = df.withColumn("rekening_masked", concat(lit("****"), col("rekening").substr(-2,2)))

# 2. Fraud Detection: > 50jt atau Luar Negeri [cite: 161, 162]
df = df.withColumn("status", when((col("jumlah") > 50000000) | (col("lokasi") == "Luar Negeri"), "FRAUD").otherwise("NORMAL"))

# 3. Encryption: Base64 untuk kolom jumlah [cite: 169, 170]
df = df.withColumn("jumlah_encrypted", base64(col("jumlah").cast("string")))

# Output ke Parquet [cite: 172]
query = df.writeStream \
    .format("parquet") \
    .option("path", "stream_data/realtime_output/") \
    .option("checkpointLocation", "data/checkpoints/") \
    .start()

query.awaitTermination()