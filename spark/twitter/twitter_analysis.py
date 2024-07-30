from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from textblob import TextBlob

# Create a Spark Context and Streaming Context
sc = SparkContext(appName="TwitterSentimentAnalysis")
ssc = StreamingContext(sc, 10)  # 10 second batch interval

# Connect to the stream of tweets
tweets = ssc.socketTextStream("localhost", 9999)

# Perform sentiment analysis on each tweet
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        sentiment = "Positive"
    elif analysis.sentiment.polarity == 0:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"
    return sentiment

# Apply the sentiment analysis to each tweet
sentiments = tweets.map(analyze_sentiment)

# Print the sentiment results
sentiments.pprint()

# Start the streaming context
ssc.start()
ssc.awaitTermination()