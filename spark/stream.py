from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.types import StructType,   StructField, StringType, IntegerType, FloatType

sc = SparkContext("local[2]", "SocketSalesAnalytics")
ssc = StreamingContext(sc, 1)
sqlContext = SQLContext(sc)


schema = StructType([
StructField("timestamp", StringType(), True),
StructField("category", StringType(), True),
StructField("product_id", StringType(), True),
StructField("quantity", IntegerType(), True),
StructField("price", FloatType(), True)
])

def process_rdd(rdd):
    if not rdd.isEmpty():
        # Convert RDD to DataFrame
        df = sqlContext.createDataFrame(rdd, schema)
        df.createOrReplaceTempView("sales")
        # Perform SQL query to calculate total sales per category
        result = sqlContext.sql("""
            SELECT category, SUM(quantity * price) as total_sales
            FROM sales
            GROUP BY category
        """)
        result.show()


lines = ssc.socketTextStream("localhost", 9999)


def parse_line(line):
    parts = line.split(",")
    return Row(timestamp=parts[0], category=parts[1], product_id=parts[2], quantity=int(parts[3]), price=float(parts[4]))

rows = lines.map(parse_line)


rows.foreachRDD(lambda rdd: process_rdd(rdd))

ssc.start()

ssc.awaitTermination()
