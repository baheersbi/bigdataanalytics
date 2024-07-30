from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext, Row
from pyspark.sql.types import StructType, StructField, StringType, FloatType


schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("sender_account", StringType(), True),
    StructField("receiver_account", StringType(), True),
    StructField("amount", FloatType(), True)
])


FRAUD_THRESHOLD = 3000.00


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

data_sources = [("localhost", 9999), ("192.168.23.148", 9999), ("192.168.1.3", 9999)]

streams = [ssc.socketTextStream(ip, port) for ip, port in data_sources]
unioned_stream = ssc.union(*streams)

transactions = unioned_stream.map(parse_line)
transactions.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
