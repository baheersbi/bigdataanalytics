# Using the current setup
If you are still running the Hadoop-Spark-Hive-Pig container from the previous session, then you can easily switch to ```spark``` using ```pyspark``` command. 

```bash
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("Books Rating Analysis") \
    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
    .getOrCreate()

# Load the CSV file from HDFS
hdfs_path = "hdfs:///home/datasrc/bigDataTask/Books_rating.csv"
books_df = spark.read.csv(hdfs_path, header=True, inferSchema=True)

# Cast the 'review/score' column to float type
books_df = books_df.withColumn("review/score", col("review/score").cast("float"))

# Show the first few rows of the DataFrame
#books_df.show()

# Select specific columns
#books_df.select("Id", "Title", "Price", "review/score").show()

# Select specific columns and filter where Price is null
#books_df.select("Id", "Title", "Price", "review/score").where(books_df["Price"].isNull()).show()

# Select specific columns and filter where Price is null
books_df.select("Id", "Title", "Price", "review/score").where(books_df["Price"].isNotNull()).show()


# Select specific columns and filter where Price is null and review/score is above 3.0
#books_df.select("Id", "Title", "Price", "review/score").where(books_df["Price"].isNull() & (books_df["review/score"] > 3.0)).show()

# Print the schema of the DataFrame
#books_df.printSchema()

# Get basic statistics
#books_df.describe().show()

# Count the number of reviews for each book
#books_df.groupBy("Title").count().show()

# Calculate the average review score for each book
#books_df.groupBy("Title").avg("review/score").show()

# Find the book with the highest average review score
#books_df.groupBy("Title").avg("review/score").orderBy("avg(review/score)", ascending=False).show(1)

# Most frequent reviewers
#books_df.groupBy("profileName").count().orderBy("count", ascending=False).show(10)

# Save the analysis result back to HDFS
#result_df = books_df.groupBy("Title").avg("review/score")
#result_df.write.csv("hdfs:///home/output/Books_rating_analysis.csv")
```
### Reading the results

```bash
# Initialize a Spark session
spark = SparkSession.builder \
    .appName("Read Analysis Result") \
    .getOrCreate()

# Path to the directory where the results are stored
result_path = "hdfs:///home/datascr/bigDataTask/Books_rating_analysis.csv"

# Read the result into a DataFrame
result_df = spark.read.csv(result_path, header=True, inferSchema=True)

# Show the results
result_df.show()
```

## Read Parquet File in Spark:
```bash
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParquetConverter") \
    .getOrCreate()

df = spark.read.parquet("/path/to/parquet/file")
df.show(1000)
spark.stop()
```

## Setting Up Logging Configuration

To reduce the verbosity of INFO log messages, follow these steps:

1. **Navigate to the Spark Configuration Directory**:

   ```sh
   cd /usr/local/spark/conf
   ```

   Copy the existing template to create a new log4j.properties file.

   ```sh
   cp log4j.properties.template log4j.properties
   ```
   
   Open the log4j.properties file in a text editor.

   ```sh
   nano log4j.properties
   ```

   Locate this line ```log4j.rootCategory=INFO, console``` (or similar), Change the logging level from ```INFO``` to ```WARN```:

   ```sh
   log4j.rootCategory=WARN, console
   ```
## Using `spark-submit`
For running a complete application, it’s more efficient to write your Spark code in a script and submit it using spark-submit. This allows you to run your Spark job as a batch process. Here’s how to do it:

1. Create a Python script, let's say in `/home/sparkscripts` and make sure that you have `sparkscripts` folder inside `home` directory and you have navigated to the `sparkscripts` folder using `cd` command.
   ```bash
   nano analyzer.py
   ```
2. Paste the previous code - presented in the begining of this page into the `analyzer.py` script and Press `ctrl+x`, Enter `Y`, and then press `Enter` to save the file.
3. Use `spark-submit` to submit it to Spark and run it as a job.
   ```bash
   spark-submit analyzer.py
   ```
## Multi-Source Data Streaming with PySpark
This section describes how to configure your PySpark Streaming application to receive and process data from multiple sources within a 192.168.x.x network. By setting up multiple socket streams and combining them using Spark's union functionality, you can handle data from several machines running `nc -lk 9999` (Mac Users) and/or `ncat -l 9999` (Windows Users).
```bash
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

# Stop any existing SparkContext
try:
    sc.stop()
except:
    pass

conf = SparkConf().setAppName("SocketTest").set("spark.driver.memory", "2g")
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 2)

# List of IP addresses of the sender machines in the 192.168.x.x network
sender_ips = ["192.168.23.148", "192.168.22.118", "192.168.22.119"]

# Create a DStream for each sender
streams = [ssc.socketTextStream(ip, 9999) for ip in sender_ips]

# Union all the streams to a single DStream
lines = ssc.union(*streams)

# Print each line received from the socket
lines.pprint()

ssc.start()
ssc.awaitTermination()
```

# Set Up the Spark Environment Locally (Optional: if you need a local setup without Docker)
1. Download and install Java by visiting this [Link](https://www.java.com/en/download/)
2. Make sure that you have ```Python``` installed in your machine. Or (Only Windows users) use Anaconda Navigator: https://docs.anaconda.com/free/navigator/install/ and try to interact with PySpark via Anaconda Prompt. 

    1.1. Type Python Or py > Hit Enter If Python Is Installed it will show the version Details Otherwise It will Open Microsoft Store To Download From Microsoft Store
3. Install ```PySpark``` using ```pip``` (Python package manager):
    ```bash
    pip install pyspark
    ```
4. Once the installation is completed, you can start the PySpark shell by running the pyspark command:
    ```bash
    pyspark
    ```
    > ### Windows troubleshooting
    > After installing PySpark, if you encounter the error message ```"The system cannot find the path specified,"``` follow the steps below:
    1. Verify that PySpark is installed correctly by typing the following command in Anaconda prompt:
        ```bash
        pip show pyspark
        ```
    2. Open Windows search and type ```Environment Variables``` go to the ```Advanced``` tab and click on ```Environment Variables```

    3. Under ```System variables``` section, click the ```New``` button. in the New System Variable dialog, enter the following:
    
        3.1. Variable name: ```PYSPARK_PYTHON```
       
        3.2. Variable value: ```C:\Users\Username\anaconda3\python.exe``` (replace with your actual Anaconda3 installation path)

    5. Similarly, click on “```New…```” under the System variables section. In the New System Variable dialog, enter the following:

        4.1. Variable name: ```PYSPARK_DRIVER_PYTHON```
        
        4.2. Variable value: ```C:\Users\Username\anaconda3\python.exe``` (replace with your actual Anaconda3 installation path)

    6. Close the Anaconda prompt and reopen it. Type ```pyspark```, wait for 5 seconds, and click "```Allow```" on the Java pop-up message.
5. The PySpark interactive shell will look something like this: 
    ```bash
    Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.1
      /_/

    Using Python version 3.11.6 (v3.11.6:8b6ee5ba3b, Oct  2 2023 11:18:21)
    Spark context Web UI available at http://172.20.10.4:4040
    Spark context available as 'sc' (master = local[*], app id = local-1717365160333).
    SparkSession available as 'spark'.      
    >>>
    ```

    > **Remember**, you can exit the PySpark shell by typing ```exit()``` or pressing ```Ctrl + D```.

6. Access the Spark Web UI at http://localhost:4040

## Spark Streaming
1. Let's create a Spark Streaming Applincation to perform real-time sales analytics (```pStream.py```):
    ```python
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

    ```
2. Run the above application:
    ```shell
    python pStream.py
    ```
3. . Open a new Command Prompt/PowerShell to start a simple data server:
   
   **Windows Users:**
   Download and install Nmap: https://nmap.org/dist/nmap-7.95-setup.exe and close all opened Command Prompt/Terminal windows. Open a new Command Prompt/Terminal Window and execute the below command. 
   ```bash
   ncat -l 9999
   ```
   **Mac Users:**
    ```bash
    nc -lk 9999
    ```
    3.1. In the Command Prompt/PowerShell where ```necat``` is running, add some sales data entries in ```CSV``` format, for example:

    ```bash
    2024-06-01 10:00:00,Electronics,1001,2,199.99
    2024-06-01 10:01:00,Books,1002,1,12.99
    2024-06-01 10:02:00,Electronics,1003,1,99.99
    2024-06-01 10:03:00,Clothing,1004,3,49.99
    2024-06-01 10:04:00,Books,1005,2,19.99

    ```

### Extended Spark Streaming Application:

        from pyspark import SparkContext
        from pyspark.streaming import StreamingContext
        from pyspark.sql import SQLContext
        from pyspark.sql import Row
        from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

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
                df = sqlContext.createDataFrame(rdd, schema)
                df.createOrReplaceTempView("sales")
                
                # Perform SQL query to calculate total sales per category
                total_sales = sqlContext.sql("""
                    SELECT category, SUM(quantity * price) as total_sales
                    FROM sales
                    GROUP BY category
                """)
                total_sales.show()

                # Perform SQL query to calculate average sales price per category
                avg_price = sqlContext.sql("""
                    SELECT category, AVG(price) as avg_price
                    FROM sales
                    GROUP BY category
                """)
                avg_price.show()

                # Perform SQL query to count the number of transactions per category
                transaction_count = sqlContext.sql("""
                    SELECT category, COUNT(*) as transaction_count
                    FROM sales
                    GROUP BY category
                """)
                transaction_count.show()

        lines = ssc.socketTextStream("localhost", 9999)

        def parse_line(line):
            parts = line.split(",")
            return Row(timestamp=parts[0], category=parts[1], product_id=parts[2], quantity=int(parts[3]), price=float(parts[4]))

        rows = lines.map(parse_line)

        rows.foreachRDD(lambda rdd: process_rdd(rdd))

        ssc.start()
        ssc.awaitTermination()
