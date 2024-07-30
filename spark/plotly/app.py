from pyspark.sql import SparkSession
import plotly.express as px

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("PySpark and Plotly Example") \
    .getOrCreate()

# Create a sample DataFrame
data = [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]
columns = ["x", "y"]
df = spark.createDataFrame(data, columns)

# Show the DataFrame
df.show()

# Collect the data to the driver for plotting
pandas_df = df.toPandas()

# Create a Plotly scatter plot
fig = px.scatter(pandas_df, x="x", y="y", title="Scatter Plot with PySpark and Plotly")

# Show the plot
fig.show()

# Stop the Spark session
spark.stop()

