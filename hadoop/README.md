## Hadoop Installation
1. Open Docker and make sure the Docker Engine is running
2. **Windows Users:** Open a Command Prompt and pull the image:
   ```bash
   docker pull suhothayan/hadoop-spark-pig-hive:2.9.2
   ```
   > ⚠️ If the download freezes at any point, cancel it by pressing ```Ctrl + C```, switch your network, and try again.

3. 🕙 Wait until the download is finished
4. 🚀 Execute this Docker command in the same window where you have pulled the image:
   ```bash
   docker run -it --name myhadoop -p 9000:9000 -p 2122:2122 -p 50070:50070 -p 50010:50010 -p 50075:50075 -p 50020:50020 -p 50090:50090 -p 8088:8088 -p 8030:8030 -p 8031:8031 -p 8032:8032 -p 8033:8033 -p 8040:8040 -p 8042:8042 -p 8080:8080 -p 8081:8081 -p 10000:10000 suhothayan/hadoop-spark-pig-hive:2.9.2 bash
   ```
   > **Troubleshooting**
   >
   > Error: ```...Ports are not available``` on Windows
   >
   > Fix: Open a Terminal (must be run as administrator) and execute ```net stop winnat``` command
   > 
   > Error: The container name "/myhadoop" is already in use
   >
   > Fix: Remove the container using Docker Desktop and re-run the ```docker run...``` command.
5. **Mac (Apple Chip M1, M2, M3) Users:** Open a Terminal and pull the image:
   ```bash
   docker pull bugbond/hadoop-spark-pig-hive-arm64
   ```
6. Run the services:
   ```bash
   docker run -it --name bigtools -p 9000:9000 -p 2122:2122 -p 50070:50070 -p 50010:50010 -p 50075:50075 -p 50020:50020 -p 50090:50090 -p 8088:8088 -p 8030:8030 -p 8031:8031 -p 8032:8032 -p 8033:8033 -p 8040:8040 -p 8042:8042 -p 8080:8080 -p 8081:8081 -p 10000:10000 bugbond/hadoop-spark-pig-hive-arm64:latest bash
   ```
8. Wait for few minutes until the prompt changes to something like this:
   ```
   * Starting OpenBSD Secure Shell server sshd                                                                    
   Waiting for hdfs to exit from safemode
   Safe mode is OFF
   Started
   root@b5dc483f5c73:/# 
   ```
   
      > **Port Number Explained**
      >
      > 2122:2122 \   # SSH
      > 
      > 50070:50070 \ # HDFS NameNode
      > 
      > 50010:50010 \ # HDFS DataNode
      > 
      > 50075:50075 \ # HDFS DataNode
      > 
      > 50020:50020 \ # SecondaryNameNode
      > 
      > 50090:50090 \ # HDFS DataNode Secure
      > 
      > 8088:8088 \   # YARN ResourceManager
      > 
      > 8030:8030 \   # YARN ResourceManager Scheduler
      > 
      > 8031:8031 \   # YARN ResourceManager Scheduler
      > 
      > 8032:8032 \   # YARN ResourceManager Scheduler
      > 
      > 8033:8033 \   # YARN ResourceManager Scheduler
      > 
      > 8040:8040 \   # YARN NodeManager
      > 
      > 8042:8042 \   # YARN NodeManager Web UI
      > 
      > 8080:8080 \   # Spark Master Web UI
      > 
      > 8081:8081 \   # Spark Worker Web UI
      > 
      > 10000:10000 \ # HiveServer2
      > 
      > **Note:** Use the below command if you exit Hadoop container and wanna re-run the created container and get access to your previous work:
      >
      > ```bash
      > docker exec -it myhadoop bash
      > ```
   To access Hadoop Web Interface, Open a browser window/tab and navigate to [http://localhost:50070](http://localhost:50070), and Spark at [http://localhost:8080](http://localhost:8080)
9. Update Ubuntu: ``` apt update ```
10. Install ``` nano ``` editor: ``` apt install nano ```
11. Verify Hadoop Installation ```ls /usr/local/hadoop```
12. Set Up Environment Variables:
    ```bash
    nano ~/.bashrc
    ```
    Add the following lines:
    ```bash
    export HADOOP_HOME=/usr/local/hadoop
    export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
    export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
    ```
    Source the ```~/.bashrc``` file:
    ```bash
    source ~/.bashrc
    ```
    > **Note:**
    > If, for any reason, Hadoop stops working, use the following commands to restart it:
    >
    > ```bash
    > stop-dfs.sh
    > stop-yarn.sh
    > start-dfs.sh
    > start-yarn.sh
    > ```
11. . Navigate to the ```home``` directory: ```cd home``` and press Enter
12. Create a new directory: ```mkdir datasrc```
13. Download this [Amazon Books Reviews](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews/data) dataset to your computer.
14. Unzip the extracted folder
15. Open a new Command Prompot or Terminal window and copy the downloaded file to the container. The container ID looks like e.g. ```3d6c17a05e33``` extracted from ```root@3d6c17a05e33:~#``` prompt.
      ```bash
      docker cp Books_rating.csv 3d6c17a05e33:/home/datasrc 
      ```
16. Create a directory in HDFS:
      ```bash
      hadoop fs -mkdir -p /home/datasrc/bigDataTask
      ```
17. Upload the file to HDFS:
      ```bash
      hadoop fs -put Books_rating.csv /home/datasrc/bigDataTask
      ```
18. Make sure the file is uploaded
      ```bash
      hadoop fs -ls /home/datasrc/bigDataTask
      ```
19. Checking the Size of the File
      ```bash
      hdfs dfs -du -h /home/datasrc/bigDataTask/Books_rating.csv
      ```
19. See the number of blocks
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
## Submit MapReduce Jobs
### Finding Highest and Lowest Review Scores
Create a directory, for instance, ```/home/scripts``` and navigate to this directory using ```cd /home/scripts``` command. Create the Mapper ```touch mapper.py``` and Reducer ```touch reducer.py``` and change their permission:
```bash
chmod 777 mapper.py reducer.py
```
Open mapper in ```nano``` editor:
```bash
nano mapper.py
```
and add the following code:
```bash
#!/usr/bin/env python
import sys
import csv
for line in sys.stdin:
    try:
        reader = csv.reader([line])
        for row in reader:
            review_score = row[6]

            if review_score:
                print('{0}'.format(review_score))
    except Exception as e:
        sys.stderr.write("Error processing line: {0} - {1}\n".format(line, str(e)))
        continue
```
Press ```ctrl+x```, type ```Y``` and press enter to close ```nano```.
And open ```reducer.py``` using ```nano```:
```bash
nano reducer.py
```
and add the below code:
```bash
#!/usr/bin/env python
import sys
highest_score = float('-inf')
lowest_score = float('inf')
for line in sys.stdin:
    line = line.strip()
    try:
        score = float(line)
        if score > highest_score:
            highest_score = score
        if score < lowest_score:
            lowest_score = score
    except ValueError:

        sys.stderr.write("Skipping invalid score: {0}\n".format(line))
        continue

print('Highest Score: {0}'.format(highest_score))
print('Lowest Score: {0}'.format(lowest_score))
```
Press ```ctrl+x```, type ```Y``` and press enter to close ```nano```.

### Submit the MapReduce Job to YARN
```bash
hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D mapreduce.job.name="FindHighestAndLowestReviewScores" \
    -input /home/datasrc/bigDataTask/Books_rating.csv \
    -output /home/dataout \
    -mapper /home/scripts/mapper.py \
    -reducer /home/scripts/reducer.py \
```
### View the Results
```bash
hadoop fs -cat /home/dataout/part-00000
```
> [!IMPORTANT]
> We highly recommend to test your scripts ```mapper.py``` and ```reducer.py``` locally before you submit it to the YARN, and ensure that it works as expected.
> ```bash
> cat /home/datasrc/bigDataTask/Books_rating.csv | python /home/scripts/mapper.py
> ```
> and 
> ```bash
> cat /home/datasrc/bigDataTask/Books_rating.csv | python /home/scripts/reducer.py
> ````
> Check if the output looks correct. If there are any errors, they should appear here and can be debugged.

### Track Specific Job Details at YARN
Open your browser and navigate to the ```http://localhost:8088``` URL. Once you're on the YARN ResourceManager web UI, you will see several sections:
 - **Running Applications**: This section shows jobs that are currently running.
 - **Finished Applications**: This section lists jobs that have completed successfully.
 - **Failed Applications**: This section lists jobs that have failed.
 - **Killed Applications**: This section shows jobs that have been manually killed.

You can click on the application ID or job name to view detailed information about a specific job. Or you can use the following commands to list or check job status:
```bash
yarn application -list
yarn application -status <application-id>
yarn application -list -appStatus
```
## Load data from HDFS to Hive
   1. Print the column names from the ```Book_rating.csv```
         ```bash
         hdfs dfs -cat /home/datasrc/bigDataTask/Books_rating.csv | head -n 1
         ```
   2. Switch to ```hive```
         ```bash
         hive
         ```
         > If you can't switch to the ```hive >``` prompt, most likely, it's due to ```Safe mode on```, so we should turn it off:
         > ```bash
         > $HADOOP_HOME/bin/hdfs dfsadmin -safemode leave
         > ```
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
   13. Some useful queries:
         ```sql
         SELECT Id, Title, Price, review_score FROM books_rating;
         
         SELECT COUNT(*) FROM books_rating;

         #  Calculate the average review score
         SELECT AVG(review_score) AS avg_review_score FROM books_rating;

         # Find the highest and lowest review scores
         SELECT 
         MAX(review_score) AS max_review_score,
         MIN(review_score) AS min_review_score 
         FROM books_rating;

         # Group by Title and calculate the average review score for each book
         SELECT 
         Title, 
         AVG(review_score) AS avg_review_score 
         FROM books_rating 
         GROUP BY Title;

         # Count the number of reviews for each user
         SELECT 
         User_id, 
         COUNT(*) AS review_count 
         FROM books_rating 
         GROUP BY User_id;

         ```
## Pig
1. Create a new CSV file
    ```sql
    id,name,age,gender
    1,John,28,M
    2,Alice,24,F
    3,Bob,35,M
    4,Carol,28,F
    ```
2. Upload it to HDFS
    ```bash
    hdfs dfs -put /home/datasrc/bigDataTask/users.csv /home/datasrc/bigDataTask/users.csv

    ```
3. Create a pig file ```touch user_analysis.pig```
    ```bash
    users = LOAD 'hdfs:///home/datasrc/bigDataTask/users.csv' USING PigStorage(',') AS (id:int, name:chararray, age:int, gender:chararray);
    users_above_25 = FILTER users BY age > 25;
    grouped_by_gender = GROUP users_above_25 BY gender;
    count_by_gender = FOREACH grouped_by_gender GENERATE group AS gender, COUNT(users_above_25) AS count;
    STORE count_by_gender INTO 'hdfs:///home/datasrc/bigDataTask/output' USING PigStorage(',');
    ```
4. Run the pig script: ```pig /root/user_analysis.pig```
5. List the output directory: ```hdfs dfs -ls /home/datasrc/bigDataTask/output```
6. Read the output file: ```hdfs dfs -cat /home/datasrc/bigDataTask/output/part-r-00000```

<!--
## Less Important Section

This is a section that contains information that is not crucial. You can keep it here for reference, but it won't be visible in the rendered README file on GitHub.

- Additional tool 1
- Additional tool 2
- Additional tool 3
-->


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
