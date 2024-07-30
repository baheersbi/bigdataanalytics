from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParquetConverter") \
    .getOrCreate()

df = spark.read.parquet("/Users/bbaheer/Downloads/yellow_tripdata_2024-01.parquet")
df.show(1000)

spark.stop()

