from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType


spark = SparkSession.builder \
    .appName("FraudDetection") \
    .getOrCreate()

schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("amount", FloatType(), True),
    StructField("timestamp", IntegerType(), True),
    StructField("location", StringType(), True)
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .load()

transactions = df.selectExpr("CAST(value AS STRING)")

transactions = transactions.withColumn("value", from_json(col("value"), schema)).select(col("value.*"))

fraudulent_transactions = transactions.filter(col("amount") > 900)

query = fraudulent_transactions \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
