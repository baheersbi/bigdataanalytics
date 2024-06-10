from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_transaction():
    return {
        "transaction_id": random.randint(1, 1000000),
        "user_id": random.randint(1, 1000),
        "amount": round(random.uniform(1.0, 1000.0), 2),
        "timestamp": int(time.time()),
        "location": random.choice(["New York", "London", "Paris", "Sydney", "Tokyo"])
    }

while True:
    transaction = generate_transaction()
    producer.send('transactions', transaction)
    time.sleep(1)
