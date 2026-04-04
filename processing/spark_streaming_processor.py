from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("SmartCityStreaming") \
    .getOrCreate()

# Schema data trip
schema = StructType([
    StructField("vendor_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("pickup_location", StringType(), True),
    StructField("dropoff_location", StringType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", DoubleType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("vehicle_type", StringType(), True)
])

# Membaca stream dari folder stream_data
df = spark.readStream \
    .schema(schema) \
    .json("stream_data/")

# Menulis hasil ke Data Lake (Parquet)
query = df.writeStream \
    .format("parquet") \
    .option("path", "data/serving/transportation") \
    .option("checkpointLocation", "checkpoints/transportation") \
    .outputMode("append") \
    .start()

query.awaitTermination()