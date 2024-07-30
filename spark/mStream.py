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
sender_ips = ["192.168.23.148"]

# Create a DStream for each sender
streams = [ssc.socketTextStream(ip, 9999) for ip in sender_ips]

# Union all the streams to a single DStream
lines = ssc.union(*streams)

# Print each line received from the socket
lines.pprint()

ssc.start()
ssc.awaitTermination()
