import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

def generate_data():
    products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Charger']
    categories = ['Electronics', 'Accessories']
    data = {
        'timestamp': datetime.now().isoformat(),
        'product_id': random.randint(1000, 9999),
        'product_name': random.choice(products),
        'category': random.choice(categories),
        'quantity_sold': random.randint(1, 20),
        'price': round(random.uniform(20.0, 500.0), 2),
        'inventory_level': random.randint(1, 100)
    }
    data['total_sales'] = data['quantity_sold'] * data['price']
    return data

def produce_data(producer, topic):
    while True:
        data = generate_data()
        producer.send(topic, value=data)
        print(f"Produced: {data}")
        time.sleep(1)

if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    produce_data(producer, 'sales_inventory')