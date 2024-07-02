import mysql.connector
import time

def get_new_fraud_transactions(cursor, last_timestamp):
    query = "SELECT transaction_id, user_id, amount, timestamp, location FROM fraud_transactions WHERE timestamp > %s"
    cursor.execute(query, (last_timestamp,))
    results = cursor.fetchall()
    print(f"Query executed: {query} with last_timestamp: {last_timestamp}")
    print(f"Number of new transactions fetched: {len(results)}")
    return results

def send_notification(fraud_transaction):
    print(f"Fraudulent transaction detected: ID {fraud_transaction[0]}, User ID {fraud_transaction[1]}, Amount {fraud_transaction[2]}, Timestamp {fraud_transaction[3]}, Location {fraud_transaction[4]}")

def main():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="fraud",
            port=3316
        )
        print("Database connection established")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    cursor = conn.cursor()

    # Initialize last_timestamp with the highest timestamp already in the table
    cursor.execute("SELECT IFNULL(MAX(timestamp), 0) FROM fraud_transactions")
    last_timestamp = cursor.fetchone()[0]
    print(f"Starting monitoring from timestamp: {last_timestamp}")

    while True:
        print("Checking for new fraud transactions...")
        new_fraud_transactions = get_new_fraud_transactions(cursor, last_timestamp)
        if new_fraud_transactions:
            print(f"Found {len(new_fraud_transactions)} new fraud transactions")
            for fraud_transaction in new_fraud_transactions:
                send_notification(fraud_transaction)
                last_timestamp = fraud_transaction[3]  # Update to the latest timestamp
        else:
            print("No new fraud transactions found.")

        time.sleep(5)

if __name__ == "__main__":
    main()
