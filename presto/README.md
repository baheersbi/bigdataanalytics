# Get Started with Presto
Apache Presto is an open-source distributed SQL query engine designed for running fast, interactive analytics across large datasets. In the context of data warehousing, Presto excels at querying data from multiple sources like relational databases (e.g., MySQL, PostgreSQL), NoSQL systems, or distributed storage (e.g., HDFS, S3) without requiring the data to be moved or transformed into a single storage location.

Here's a practical example of setting up Apache Presto with MySQL, PostgreSQL, and Kafka using Docker and Docker networking.

## Create a Docker Network
```bash
docker network create prestonet
```
## Run the Presto Container
```bash
docker run --name presto --network prestonet -p 8080:8080 -ti prestodb/presto:latest

```
## Run the MySQL container 
```bash
docker run --name prestomysql -p 3320:3306 --network prestonet -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=testdb -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpassword -d mysql
```

## Run the PostgreSQL container
```bash
docker run --name postgres -p 5433:5432 --network prestonet -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpassword -e POSTGRES_DB=testdb -d postgres
```
## Configuration Files
You'll need to configure the connectors for MySQL, PostgreSQL, and Kafka.

### Enter your Presto container:
```bash
docker exec -ti presto bash
```
Update the OS:
```bash
dnf udpate
```
Install ```nano``` editor:
```bash
dnf install nano
```
and navigate to the ```catalog``` directory as follow:
 ```bash
 cd /opt/presto-server/etc/catalog
 ```
### MySQL Connector
Create ```mysql.properties``` file in the ```catalog``` director:

```bash
touch mysql.properties
```
Now edit the ```nano mysql.properties``` file and add the following lines: 

```bash
connector.name=mysql
connection-url=jdbc:mysql://172.26.0.2:3306
connection-user=root
connection-password=rootpassword
```

### PostgreSQL Connector
Create ```postgresql.properties``` file in the ```catalog``` director:

```bash
touch postgresql.properties
```
Now edit the ```nano postgresql.properties``` file and add the following lines: 

```bash
connector.name=postgresql
connection-url=jdbc:postgresql://postgres:5432/testdb
connection-user=testuser
connection-password=testpassword
```