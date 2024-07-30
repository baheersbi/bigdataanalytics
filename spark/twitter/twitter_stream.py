import tweepy
import socket
import json

# Twitter API credentials
API_KEY = "trn7rW3uBBIBFYvKQgnzXBZw7"
API_SECRET_KEY = "dEm8AwypbpyL2xzfFkKFPq3VSMKstdihyjhc09jVdamy3T7R7C"
ACCESS_TOKEN = "469115347-52LEwIeCY7bDa93wIcU8dabIzN1WqwW2xTp8JVtU"
ACCESS_TOKEN_SECRET = "YbhKlcnYkyGgSz81OiVjZqSqvlt5Wq1Ogys0SOWFAi6nv"

class TweetListener(tweepy.StreamListener):
    def __init__(self, socket):
        super(TweetListener, self).__init__()
        self.client_socket = socket

    def on_data(self, data):
        try:
            message = json.loads(data)
            tweet = message.get('text')
            if tweet:
                print(f"Tweet: {tweet}")
                self.client_socket.send((tweet + "\n").encode('utf-8'))
            return True
        except BaseException as e:
            print(f"Error on_data: {str(e)}")
        return True

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        if status_code == 420:
            return False  # disconnect stream if rate limited
        return True

def stream_tweets(socket):
    # Set up Tweepy authorization and API access
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create Tweepy stream
    listener = TweetListener(socket)
    stream = tweepy.Stream(auth, listener)

    # Filter Twitter Streams to capture data by keywords
    stream.filter(track=["python", "spark", "big data"], languages=["en"])

if __name__ == "__main__":
    s = socket.socket()
    s.bind(("localhost", 9999))  # Ensure the port is not in use or change the port number
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print("Connected. Streaming tweets...")
    stream_tweets(conn)