# Quickstart
This quickstart guide will assist you in setting up your local machine in just three easy steps. Please ensure that Docker, Docker Compose, and Git are already installed.
## Get superset
1. Open a Terminal/Command Prompt window and execute the below command: 
    ```bash
    git clone https://github.com/apache/superset
    ````
2. Enter the repository you just cloned:
    ```bash
    cd superset
    ```
3. Set the repo to the state associated with the latest official version
   ```bash
   $ git checkout tags/5.0.0
   ```
4. Fire up Superset using Docker Compose
    ```bash
    docker compose -f docker-compose-image-tag.yml up
    ```
5. Login to Superset

    * Next, go to http://localhost:8088 and log in using the default account that was created.

    ```bash
    username: admin
    password: admin
    ```
## Run MySQL
1. Create a MySQL container (Crypto) and it should be added to the Superset Network (superset_default):
    ```bash
    docker run --name Crypto --network superset_default -e MYSQL_ROOT_PASSWORD=123456 -p 3312:3306 -d mysql:latest
    ```
2. Login to MySQL
3. Create a database
    ```bash
    CREATE DATABASE crypto;
    ```
4. Use the ```crypto``` database and create a table ```transactions```
    ```sql
    USE crypto;

    CREATE TABLE transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_id INT,
        timestamp DATETIME,
        crypto_type VARCHAR(50),
        amount DECIMAL(10, 4),
        price DECIMAL(10, 2)
    );
    ```
## Install Kafka Python client:
```bash
pip install kafka-python
```
### Install MySQL Python client
```bash
pip install mysql-connector-python
```
## Produce some transactions:

The ```producer.py``` script is used to produce some dummy data and store it in a Kafka topic. Download ```producer.py``` and run it ```python producer.py```.

## Consume transactions
The ```consumer.py``` script will consumer the ctypto transactions fromt the Kafka topic and store them in MySQL. 

## Connect Superset to MySQL
In the Superset UI, when adding a new database connection, use the internal Docker network hostname ```Crypto``` and the port ```3306``` (the internal port within the Docker network). 

Connection Details: 
```bash
	-	HOST: Crypto
	-	PORT: 3306
	-	DATABASE NAME: crypto
	-	USERNAME: root
	-	PASSWORD: 123456
	-	DISPLAY NAME: MySQL
```


