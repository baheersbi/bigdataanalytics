from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, Row
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Define the transaction schema
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("sender_account", StringType(), True),
    StructField("receiver_account", StringType(), True),
    StructField("amount", FloatType(), True)
])

# Threshold for flagging transactions as potential fraud
FRAUD_THRESHOLD = 3000.00

# Initialize Spark context
conf = SparkConf().setAppName("FraudDetectionApp")
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 5)  # 5-second batch interval
sqlContext = SQLContext(sc)

def process_rdd(time, rdd):
    try:
        if not rdd.isEmpty():
            df = sqlContext.createDataFrame(rdd, schema)
            df.createOrReplaceTempView("transactions")
            fraud_transactions = sqlContext.sql(f"""
                SELECT * FROM transactions WHERE amount > {FRAUD_THRESHOLD}
            """)
            fraud_transactions.show()
    except Exception as e:
        print(f"Error processing RDD: {e}")

def parse_line(line):
    parts = line.split(",")
    return Row(
        timestamp=parts[0],
        sender_account=parts[1],
        receiver_account=parts[2],
        amount=float(parts[3])
    )

lines = ssc.socketTextStream("localhost", 9999)
transactions = lines.map(parse_line)
transactions.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
