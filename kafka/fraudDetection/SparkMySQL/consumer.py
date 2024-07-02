# consumer.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
import mysql.connector

spark = SparkSession.builder \
    .appName("FraudDetection") \
    .config("spark.jars", "/Users/bbaheer/Downloads/mysql-connector-j-8.4.0/mysql-connector-j-8.4.0.jar") \
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

transactions = df.selectExpr("CAST(value AS STRING)") \
    .withColumn("value", from_json(col("value"), schema)) \
    .select(col("value.*"))

fraudulent_transactions = transactions.filter(col("amount") > 900)

def process_batch(df, epoch_id):
    pdf = df.toPandas()

    if not pdf.empty:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="fraud",
            port=3316
        )
        cursor = conn.cursor()

        for index, row in pdf.iterrows():
            cursor.execute("INSERT INTO fraud_transactions (transaction_id, user_id, amount, timestamp, location) VALUES (%s, %s, %s, %s, %s)",
                           (row['transaction_id'], row['user_id'], row['amount'], row['timestamp'], row['location']))

        conn.commit()
        cursor.close()
        conn.close()

    for index, row in pdf.iterrows():
        print(f"Fraudulent transaction detected: {row['transaction_id']} for amount {row['amount']}")


query = fraudulent_transactions.writeStream \
    .outputMode("append") \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()
