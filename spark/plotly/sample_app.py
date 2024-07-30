from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()

data = [("James", "Smith"), ("Anna", "Rose"), ("Robert", "Williams")]
columns = ["firstname", "lastname"]
df = spark.createDataFrame(data, columns)

df.show()

spark.stop()

