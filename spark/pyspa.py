from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, desc, split, year, from_unixtime, concat_ws, collect_list
import os
spark = SparkSession.builder.appName("demo").getOrCreate()
file_path = os.path.expanduser("/Users/bbaheer/Downloads/Books_rating.csv");
df = spark.read.csv(file_path, header=True, inferSchema=True)
# df.printSchema()
# df.show(5)
# review_count = df.count();
# print(f"Total Number of Reviews: {review_count}")

df = df.withColumnRenamed("review/score", "review_score") \
       .withColumnRenamed("review/helpfulness", "review_helpfulness") \
       .withColumnRenamed("review/time", "review_time") \
       .withColumnRenamed("review/summary", "review_summary") \
       .withColumnRenamed("review/text", "review_text")

# avg_score=df.select(avg("review_score")).first()[0]
# print(f"The average of scores: {avg_score}")


score_distribution = df.groupBy("review_score").count().orderBy(desc("count"))
score_distribution.show()


# top_books = df.groupBy("Title").count().orderBy(desc("count")).limit(10)
# print("Top 10 Most Reviewed Books:")
# top_books.show(truncate=False)