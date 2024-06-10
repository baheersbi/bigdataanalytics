# Apache Kafka 

1. Get the Docker image:
    ```bash
    docker pull apache/kafka:3.7.0
    ```
2. Run a Kafka container:
    ```bash
    docker run --name mykafka -p 9092:9092 apache/kafka:3.7.0
    ```
3. Create a topic (test):
    ```bash
    docker exec -it mykafka /opt/kafka/bin/kafka-topics.sh --create --topic test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
4. Start the Kafka producer. Open a new Command Prompt window and run the following command:
    ```bash
    docker exec -it mykafka /opt/kafka/bin/kafka-console-producer.sh --topic test --bootstrap-server localhost:9092
    ```
    The prompt will enable you to enter your messages. So, start typing messages and you will read it in the bellow Kafka Consumer.
5. Read the events. Open a new Command Prompt window and run the following command:
    ```bash
    docker exec -it mykafka /opt/kafka/bin/kafka-console-consumer.sh --topic test --from-beginning --bootstrap-server localhost:9092
    ```
6. Install Python package:
    ```bash
    python3 -m pip install spark-sql-kafka
    ```
7. Download the ```producer.py``` and ```consumer.py``` files and run the ```producer.py``` file. Make sure to navigate to the folder where the files are located. 
    ```bash
    python producer.py
    ``` 
    and now run the ```consumer.py``` script. 
    ```bash
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 consumer.py
    ```