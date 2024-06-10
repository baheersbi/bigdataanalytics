from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark = SparkSession.builder \
    .appName("CourierETA") \
    .getOrCreate()

schema = StructType([
    StructField("courier_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("timestamp", TimestampType(), True)
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "courier-locations") \
    .load()

df = df.selectExpr("CAST(value AS STRING)") \
       .select(from_json(col("value"), schema).alias("data")) \
       .select("data.*")


df = df.withColumn("estimated_arrival_time", expr("timestamp + INTERVAL 30 MINUTES"))

query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
