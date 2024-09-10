from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

crypto_types = ['Bitcoin', 'Ethereum', 'Ripple', 'Litecoin', 'Cardano']
account_ids = [1, 2, 3, 4, 5]

def create_transaction():
    return {
        'account_id': random.choice(account_ids),
        'timestamp': datetime.now().isoformat(),
        'crypto_type': random.choice(crypto_types),
        'amount': round(random.uniform(0.01, 10), 4),
        'price': round(random.uniform(30000, 60000), 2)
    }

while True:
    transaction = create_transaction()
    producer.send('crypto_transactions', transaction)
    print(f"Sent: {transaction}")
    time.sleep(1)