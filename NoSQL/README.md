# Using Apache Cassandra with Docker
1. Pull the Docker image:
   ```bash
   docker pull cassandra
   ```
2. Create a Docker Network:
   ```bash
   docker network create cassandra-net
   ```
3. Start the Seed Node:
   ```bash
   docker run --name cassandra-seed   --network cassandra-net   --hostname cassandra-seed   -p 9043:9042   -m 2g --memory-swap 3g   -e MAX_HEAP_SIZE=1024M   -e HEAP_NEWSIZE=256M  -d cassandra
   ```
4. Start two additional nodes:
   ```bash
   docker run --name cassandra-node1 --network cassandra-net --hostname cassandra-node1 -p 9044:9042 -m 2g --memory-swap 3g -e CASSANDRA_SEEDS=cassandra-seed -e MAX_HEAP_SIZE=1024M -e HEAP_NEWSIZE=256M -d cassandra
   ```
   ```bash
   docker run --name cassandra-node2 --network cassandra-net --hostname cassandra-node2 -p 9045:9042 -m 2g --memory-swap 3g -e CASSANDRA_SEEDS=cassandra-seed -e MAX_HEAP_SIZE=1024M -e HEAP_NEWSIZE=256M -d cassandra
   ```
5. Inspect the network configuration:
    ```bash
   docker network inspect cassandra-net
    ```
6. Check the status of your nodes:
    ```bash
    docker exec -it cassandra-seed nodetool status
    ```
   > ***Note:*** Identify which node is the seed node:
   >
   > ```bash
   > docker exec -it cassandra-node1 cat /etc/cassandra/cassandra.yaml | grep -i seeds
   > ```
   > ```bash
   > docker exec -it cassandra-node2 cat /etc/cassandra/cassandra.yaml | grep -i seeds
   > ```
   > ```bash
   > docker exec -it cassandra-seed cat /etc/cassandra/cassandra.yaml | grep -i seeds
   > ```
7. Start Bash Shell in Cassandra Container (Seed Node):
   ```bash
   docker exec -it cassandra-seed bash
   ```    
8. Update the package index from sources:
   ```bash
   apt update
   ```
9. Install the ```nano``` editor:
   ```bash
   apt install nano
   ```
9. Increment request timeout:
   8.1. Navigate to cassandra folder
   ```bash
   cd ~/.cassandra/
   ```
   > If it fails to switch to the ```.cassandra``` folder, then you should create it ```mkdir -p ~/.cassandra```
   
   8.2. Create or edit the ```cqlshrc``` file:
   ```bash
   nano ~/.cassandra/cqlshrc
   ```
   8.4. Add the following two lines and save and exit ```nano``` (```Ctrl + O``` to save, Enter, then ```Ctrl + X``` to exit).
   ```bash
   [authentication]
   username = your_username
   password = your_password
   
   [connection]
   request_timeout = 6000
   ```
6. Switch to Cassandra SQL Prompt:
   ```bash
   cqlsh
   ```
8. Verify the Data Center Names:
   ```bash
   SELECT data_center FROM system.local;
   ```
   
   ```bash
   SELECT peer, data_center FROM system.peers;
   ``` 
9. Create a ```KEYSPACE```:
   ```bash
   CREATE KEYSPACE iot_data WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': 3};
   ```
10. Verify if the ```KEYSPACE``` named ```iot_data``` is created
   ```bash
   DESCRIBE KEYSPACES;
   ```
11. Use the ```iot_data``` Keyspace:
    ```bash
    USE iot_data
    ```
12. Create a table
   ```sql
   CREATE TABLE example_table (
    id UUID PRIMARY KEY,
    name text,
    age int,
    email text
   );

   ```
12. Verify if the table is created:
    ```bash
    DESCRIBE TABLES;
    ```
13. Verify if the data is replicated.
    13.1. Enter the node1 by opening a new Command Prompt/Terminal window and type ```docker exec -it cassandra-node1 cqlsh``` and press Enter. This will take you to the Cassandra SQL Shell and now you can list the KEYSPACES created in the Seed Node (cassandra-seed) ```DESCRIBE KEYSPACES;```. The ```iot_data``` Keyspace should list.

14. Insert some data:
    ```sql
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Alice Johnson', 29, 'alice.johnson@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Bob Smith', 34, 'bob.smith@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Charlie Brown', 22, 'charlie.brown@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'David Wilson', 45, 'david.wilson@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Eva Adams', 31, 'eva.adams@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Frank Miller', 28, 'frank.miller@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Grace Lee', 37, 'grace.lee@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Henry Walker', 26, 'henry.walker@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Isabella Martinez', 33, 'isabella.martinez@example.com');
    INSERT INTO example_table (id, name, age, email) VALUES (uuid(), 'Jack Davis', 40, 'jack.davis@example.com');

    ```
## Primary Key Structure (Partition Key)
   ```sql
   CREATE TABLE users (
    user_id UUID,
    name text,
    age int,
    email text,
    country text,
    PRIMARY KEY (country, user_id)
   );
   ```
   > - ```country``` is the **partition** key.
   >    - The partition key (```country```) determines how the data is distributed across nodes. Rows with the same country value are stored on the same node, making queries that filter by country efficient.
   > - ```user_id``` is the clustering column.

   ```sql
   INSERT INTO users (user_id, name, age, email, country) VALUES (uuid(), 'Alice Johnson', 29, 'alice.johnson@example.com', 'USA');
   INSERT INTO users (user_id, name, age, email, country) VALUES (uuid(), 'Bob Smith', 34, 'bob.smith@example.com', 'Canada');
   INSERT INTO users (user_id, name, age, email, country) VALUES (uuid(), 'Charlie Brown', 22, 'charlie.brown@example.com', 'USA');
   INSERT INTO users (user_id, name, age, email, country) VALUES (uuid(), 'David Wilson', 45, 'david.wilson@example.com', 'UK');
   ```
### Tracing Queries
   ```sql
   TRACING ON;
   SELECT * FROM users WHERE country = 'USA';
   TRACING OFF;
   ```
