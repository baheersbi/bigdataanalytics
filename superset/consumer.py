from kafka import KafkaConsumer
import mysql.connector
import json

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="crypto",
    port=3310
)
cursor = conn.cursor()

# Kafka consumer setup
consumer = KafkaConsumer(
    'crypto_transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    account_id = transaction['account_id']
    timestamp = transaction['timestamp']
    crypto_type = transaction['crypto_type']
    amount = transaction['amount']
    price = transaction['price']

    # Insert transaction into MySQL
    cursor.execute(
        "INSERT INTO transactions (account_id, timestamp, crypto_type, amount, price) VALUES (%s, %s, %s, %s, %s)",
        (account_id, timestamp, crypto_type, amount, price)
    )
    conn.commit()
    print(f"Written to MySQL: {transaction}")