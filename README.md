# Big Data Analytics
## Hadoop Installation
# Easy approach:
1. Open Docker
2. Search for ```suhothayan/hadoop-spark-pig-hive``` image
3. ```Pull``` the image
4. Open a Command Prompt or Terminal
5. Execute this Docker command:
   ```bash
     docker run -it --name myhadoop \
     -p 2122:2122 \    # SSH
     -p 50070:50070 \  # HDFS NameNode
     -p 50010:50010 \  # HDFS DataNode
     -p 50075:50075 \  # HDFS DataNode
     -p 50020:50020 \  # HDFS DataNode
     -p 50090:50090 \  # HDFS DataNode
     -p 8088:8088 \    # YARN ResourceManager
     -p 8030:8030 \    # YARN ResourceManager scheduler
     -p 8031:8031 \    # YARN ResourceManager scheduler
     -p 8032:8032 \    # YARN ResourceManager scheduler
     -p 8033:8033 \    # YARN ResourceManager scheduler
     -p 8040:8040 \    # YARN NodeManager
     -p 8042:8042 \    # YARN NodeManager
     -p 8080:8080 \    # Spark Master
     -p 8081:8081 \    # Spark Worker
     -p 10000:10000 \  # HiveServer2
     suhothayan/hadoop-spark-pig-hive bash

   ```
   > **Note:** Use the below command if you exit Hadoop container and wanna re-run the created container and get access to your previous work:
   >
   > ```bash
   > docker exec -it myhadoop bash
   > ```
   To access Hadoop Web Interface, Open a browser window/tab and navigate to ```http://localhost:50070```, and Spark at ```http://localhost:8080``` 
6. Navigate to the ```home``` directory: ```cd home``` and press Enter
7. Create a new directory: ```mkdir datasrc```
8. Download this [Amazon Books Reviews](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews/data) dataset to your computer.
9. Unzip the extracted folder
10. Open a new Command Prompot or Terminal window and copy the downloaded file to the container. The container ID looks like ```3d6c17a05e33``` extracted from ```root@3d6c17a05e33:~#``` prompt.
      ```bash
      docker cp Books_rating.csv 3d6c17a05e33:/home/datasrc 
      ```
11. Create a directory in HDFS:
      ```bash
      hadoop fs -mkdir -p /home/datasrc/bigDataTask
      ```
12. Upload the file to HDFS:
      ```bash
      hadoop fs -put Book_rating.csv /home/datasrc/bigDataTask
      ```
13. Make sure the file is uploaded
      ```bash
      hadoop fs -ls /home/datasrc/bigDataTask
      ```
14. See the number of blocks
      ```bash
      hadoop fsck /home/datasrc/bigDataTask
      ```
> ***Note***
> 
> Create a directory in HDFS: ```hdfs dfs -mkdir -p /user/root/test```
> 
> Remove a directory in HDFS: ```hdfs dfs -rm -r /user/root/test```
> 
> List files/folders in HDFS: ```hdfs dfs -ls /user/root```
## Load data from HDFS to Hive
   1. Print the column names from the ```Book_rating.csv```
         ```bash
         hdfs dfs -cat /home/datasrc/bigDataTask/Books_rating.csv | head -n 1
         ```
   2. Switch to ```hive```
         ```bash
         hive
         ```
   3. Show the current Databases ```show databases``` and it will return an error. Leave the ```hive``` prompt by typing ```exit;```
   4. Remove the ```metastore_db``` folder: ```rm -rf metastore_db```
   5. Initialize the database schema for Apache Hive
         ```bash
         schematool -dbType derby -initSchema
         ```
   6. Switch back to ```hive```
   7. List databases and it won't return any error: ```show databases;```
   8. Create a new database ```create database amazonDB;```
   9. Use the new database ```use amazonDB;```
   10. Define the Hive Table Schema
         ```sql
         CREATE TABLE books_rating (
         Id STRING,
         Title STRING,
         Price STRING,
         User_id STRING,
         profileName STRING,
         review_helpfulness STRING,
         review_score FLOAT,
         review_time BIGINT,
         review_summary STRING,
         review_text STRING
         )
         ROW FORMAT DELIMITED
         FIELDS TERMINATED BY ','
         LINES TERMINATED BY '\n'
         TBLPROPERTIES ('skip.header.line.count'='1');

         ```
   11. Load Data into the Hive Table
         ```sql
         LOAD DATA INPATH '/home/datasrc/bigDataTask/Books_rating.csv' INTO TABLE books_rating;
         ```
   12. Verify the data
         ```sql
         SELECT * FROM books_rating LIMIT 10;
         ```
   13.   

14. Pig
   ```pig
   cat <<EOF > /root/user_analysis.pig
   users = LOAD 'hdfs:///home/datasrc/bigDataTask/users.csv' USING PigStorage(',') AS (id:int, name:chararray, age:int, gender:chararray);
   users_above_25 = FILTER users BY age > 25;
   grouped_by_gender = GROUP users_above_25 BY gender;
   count_by_gender = FOREACH grouped_by_gender GENERATE group AS gender, COUNT(users_above_25) AS count;
   STORE count_by_gender INTO 'hdfs:///home/datasrc/output' USING PigStorage(',');
   EOF
   ```
11. Using Pig Prompt (```grunt>```)
grunt> reviews = LOAD 'hdfs:///home/datasrc/bigDataTask/Books_rating.csv' USING PigStorage(',') AS (
    reviewerID:chararray,
    asin:chararray,
    reviewerName:chararray,
    helpful:chararray,
    reviewText:chararray,
    overall:int,
    summary:chararray,
    unixReviewTime:long,
    reviewTime:chararray
);

12. 

# A detailed approach 
> The objective of this approach is to teach students some basic Linux commands, as well as Hadoop installation. 

This guide will help you step-by-step in building a custom Ubuntu Docker image, setting up Hadoop for data processing.

## Getting Started: Building Your Docker Image

Docker lets you create virtual environments called "containers" to run software. We'll build an Ubuntu container that has a root (admin) password.

### 1. Create a `Dockerfile`
A `Dockerfile` is like a recipe that tells Docker how to create the environment.

- Create a new file named `Dockerfile` (without any file extension).
  - Windows users:
    - Open PowerShell
    - Create a new directory: `mkdir hadoop`
    - Change your directory: `cd hadoop`
    - Create the Dockerfile: `echo $null >> Dockerfile`
    - Edit the Dockerfile: `notepad.exe Dockerfile`
- Copy this code into the `Dockerfile`:
    ```Dockerfile
    FROM ubuntu
    RUN echo 'root:Docker!' | chpasswd
    ```
  - `FROM ubuntu`: Starts with a basic Ubuntu system.
  - `RUN`: Sets a root password to `Docker!`.

### 2. Build the Docker Image

- Open your terminal or command prompt and navigate to the folder with your `Dockerfile`.
- Run this command:
    ```bash
    docker build -t bubuntu .
    ```
  - `-t bubuntu`: Names the image `bubuntu`.

### 3. Run the Docker Container

- Create and start the container:
    ```bash
    docker run -it --name hadoop-container -p 9870:9870 -p 9864:9864 -p 8088:8088 -p 8042:8042 -p 19888:19888 -p 10020:10020 bubuntu
    ```
  - `-it`: Makes the terminal interactive.
  - `-p`: Connects the port of your computer to the container.

## Preparing Ubuntu for Hadoop

### 1. Update System Packages and Create user for Hadoop environment

- Make sure your system is up to date:
    ```bash
    apt update -y
    ```
- Install ```adduser```
   ```bash
    apt install adduser
   ```
- Create user for Hadoop environment
   ```bash
    adduser hadoop
   ```
- Add ```hadoop``` user to the ```sudo``` Group:
  ```bash
  usermod -aG sudo hadoop
  ```
### 2. Install Java

- Java is needed for Hadoop:
    - Java Development Kit (JDK):
        ```bash
        apt install openjdk-8-jdk -y
        ```
    - Verify Java Installation:
       ```bash
        java -version
        ```
### 3. Install `wget`, `sudo`, and `nano` editor

- `wget` is a tool to download files:
    ```bash
    apt install wget nano sudo -y
    ```
### 4. Install OpenSSH (Server and Client)
   ```bash
    apt install openssh-server openssh-client -y
   ```
### 5. Switch to the created user
   ```bash
   su - hadoop
   ```
### 6. Generate SSH keys (Public and Private)
  ```bash
  ssh-keygen -t rsa
  ```
### 7. Add the public key to `authorized_keys`
 ```bash
 sudo cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
 ```
### 8. Change the permissions of the `authorized_keys` file
 ```bash
 sudo chmod 640 ~/.ssh/authorized_keys
 ```
### 9. Restart SSH service
 ```bash
 sudo service ssh restart
 ```
### 10. Verify the Passwordless SSH connection
 ```bash
 ssh localhost
 ```
## Hadoop Installation and Configuration

### 1. Download and Extract Hadoop

- Download Hadoop:
    ```bash
    wget https://downloads.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz
    ```
- Extract the downloaded file:
    ```bash
    tar -xzvf hadoop-3.4.0.tar.gz
    ```
- Move the extracted folder:
    ```bash
    sudo mv hadoop-3.4.0 /usr/local/hadoop
    ```
- Configuring Java Environment Variables for Hadoop Setup
   ```bash
    dirname $(dirname $(readlink -f $(which java)))
    ```
- Create a directory to store logs
  ```bash
  sudo mkdir /usr/local/hadoop/logs
  ```
- Change the ownership of the `/usr/local/hadoop` to the user `hadoop`:
  ```bash
  sudo chown -R hadoop:hadoop /usr/local/hadoop
  ```
### 3. Configure Hadoop

#### Set Up Environment Variables

- Open the `.bashrc` file for editing:
    ```bash
    sudo nano ~/.bashrc
    ```
- Add these lines to the file:
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-arm64
    export HADOOP_HOME=/usr/local/hadoop
    export HADOOP_INSTALL=$HADOOP_HOME
    export HADOOP_MAPRED_HOME=$HADOOP_HOME
    export HADOOP_COMMON_HOME=$HADOOP_HOME
    export HADOOP_HDFS_HOME=$HADOOP_HOME
    export YARN_HOME=$HADOOP_HOME
    export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
    export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
    export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
    ```
- Save and exit `nano` (Ctrl + O to save, Enter, then Ctrl + X to exit).
- Load the new settings:
    ```bash
    source ~/.bashrc
    ```
- Edit `hadoop-env.sh` file
  ```bash
  sudo nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
  ```
  - Add the following lines
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-arm64
    export HADOOP_HOME_WARN_SUPPRESS=1
    export HADOOP_ROOT_LOGGER="WARN,DRFA"
    ```
- Save and exit `nano` (Ctrl + O to save, Enter, then Ctrl + X to exit).
- Locate the correct Java path
  ```bash
    which javac
  ```
  - Determine the Path of javac
    ```bash
    readlink -f /usr/bin/javac
    ```
#### Configure Hadoop Files

- Edit these files in the Hadoop folder:

##### `core-site.xml`

- Open this file:
    ```bash
    sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
    ```
- Add the following configuration:
    ```xml
    <configuration>
      <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
      </property>
      <property>
        <name>hadoop.tmp.dir</name>
        <value>/usr/local/hadoop/tmp</value>
        <description>Temporary directories base.</description>
      </property>
    </configuration>
    ```
- Save and exit.

##### `hdfs-site.xml`

- Open the file:
    ```bash
    sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
    ```
- Add this content:
    ```xml
    <configuration>
      <property>
        <name>dfs.replication</name>
        <value>1</value>
      </property>
      <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/hdfs/namenode</value>
      </property>
      <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/hdfs/datanode</value>
      </property>
    </configuration>
    ```
- Save and exit.

##### `mapred-site.xml`

- Open the file:
    ```bash
    sudo nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
    ```
- Add this:
    ```xml
    <configuration>
      <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
      </property>
    </configuration>
    ```
- Save and exit.

##### `yarn-site.xml`

- Open this file:
    ```bash
    sudo nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
    ```
- Add the following:
    ```xml
    <configuration>
      <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
      </property>
      <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
      </property>
      <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>localhost</value>
      </property>
    </configuration>
    ```
- Save and exit.

## Starting Hadoop Services

- Format HDFS NamdeNode
  ```bash
  hdfs namenode -format
  ```
- Start Hadoop services:
    ```bash
    start-all.sh
    ```
- Or start each service separately:
  - Start Hadoop Cluster
    ```bash
    start-dfs.sh
    ```
  - Start the YARN
    ```bash
    start-yarn.sh
    ```
- Verify all the running components
  ```bash
    jps
  ```
- Create directories and upload a file:
    ```bash
    hadoop fs -mkdir /fbi-simulation
    hadoop fs -put simulation_data.csv /fbi-simulation
    ```
- Check the Hadoop file system (HDFS):
    ```bash
    hadoop fs -ls /fbi-simulation
    ```
- Explore and analyze the data as needed!

### Access Hadoop Web Interface

- **NameNode Web UI** (for HDFS status): Open `http://localhost:9870` in your web browser.
- **ResourceManager Web UI** (for YARN status): Open `http://localhost:8088`.

### Stopping Hadoop Services

- Stop all Hadoop services:
    ```bash
    stop-all.sh
    ```
