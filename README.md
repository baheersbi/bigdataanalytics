# Big Data Analytics
## Hadoop Installation

# Setting Up Ubuntu Docker Image with Hadoop 

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
    docker run -it -p 9870:9870 bubuntu
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
    - Java Runtime Environment (JRE):
        ```bash
        apt install default-jre -y
        ```
    - Java Development Kit (JDK):
        ```bash
        apt install default-jdk -y
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
    wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
    ```
- Extract the downloaded file:
    ```bash
    tar -xzvf hadoop-3.3.6.tar.gz
    ```
- Move the extracted folder:
    ```bash
    sudo mv hadoop-3.3.6 /usr/local/hadoop
    ```
- Configuring Java Environment Variables for Hadoop Setup
   ```bash
    dirname $(dirname $(readlink -f $(which java)))
    ```
### 3. Configure Hadoop

#### Set Up Environment Variables

- Open the `.bashrc` file for editing:
    ```bash
    sudo nano ~/.bashrc
    ```
- Add these lines to the file:
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
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
  - Add the following line
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
    ```
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
