# Big Data Analytics
## Hadoop Installation

# Setting Up Ubuntu Docker Image with Hadoop 

This guide will help you step-by-step in building a custom Ubuntu Docker image, setting up Hadoop for data processing.

## Getting Started: Building Your Docker Image

Docker lets you create virtual environments called "containers" to run software. We'll build an Ubuntu container that has a root (admin) password.

### 1. Create a `Dockerfile`
A `Dockerfile` is like a recipe that tells Docker how to create the environment.

- Create a new file named `Dockerfile` (without any file extension).
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
### 2. Install Java

- Java is needed for Hadoop:
    ```bash
    apt install default-jre -y
    ```

### 3. Install `wget`

- `wget` is a tool to download files:
    ```bash
    apt install wget -y
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
    mv hadoop-3.3.6 /usr/local/hadoop
    ```

### 2. Install `nano` Editor

- Install the text editor `nano` to edit files:
    ```bash
    apt install nano -y
    ```

### 3. Configure Hadoop

#### Set Up Environment Variables

- Open the `.bashrc` file for editing:
    ```bash
    nano ~/.bashrc
    ```
- Add these lines to the file:
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
    export HADOOP_HOME=/usr/local/hadoop
    export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
    ```
- Save and exit `nano` (Ctrl + O to save, Enter, then Ctrl + X to exit).
- Load the new settings:
    ```bash
    source ~/.bashrc
    ```

#### Configure Hadoop Files

- Edit these files in the Hadoop folder:

##### `core-site.xml`

- Open this file:
    ```bash
    nano $HADOOP_HOME/etc/hadoop/core-site.xml
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
    nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
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
    nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
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
    nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
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

## Configuring SSH for Hadoop

Hadoop needs SSH to manage data.

### 1. Install SSH Server

- Install OpenSSH server:
    ```bash
    apt-get update && apt-get install -y openssh-server
    ```

### 2. Set Up SSH Keys

- Generate SSH keys:
    ```bash
    ssh-keygen -t dsa -P '' -f ~/.ssh/id_rsa
    ```
- Add the public key to authorized keys:
    ```bash
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    ```
- Set correct permissions:
    ```bash
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_keys
    ```

### 3. Update SSH Configuration

- Open the SSH config file:
    ```bash
    nano /etc/ssh/sshd_config
    ```
- Ensure these options are enabled:
    ```bash
    PasswordAuthentication yes
    PermitRootLogin yes
    ```
- Save and restart SSH:
    ```bash
    service ssh restart
    ```

### 4. Test SSH Access

- Try to connect locally:
    ```bash
    ssh localhost
    ```
- To exit, type `exit`.

## Starting Hadoop Services

### Define More Environment Variables

- Add these variables to `.bashrc`:
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
    export PATH=$PATH:/usr/lib/jvm/java-11-openjdk-arm64/bin
    export HADOOP_HOME=/usr/local/hadoop
    export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
    export HADOOP_MAPRED_HOME=$HADOOP_HOME
    export YARN_HOME=$HADOOP_HOME
    export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
    export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
    export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
    export HADOOP_STREAMING=$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
    export HADOOP_LOG_DIR=$HADOOP_HOME/logs
    export PDSH_RCMD_TYPE=ssh

    export HDFS_NAMENODE_USER=root
    export HDFS_DATANODE_USER=root
    export HDFS_SECONDARYNAMENODE_USER=root
    export YARN_RESOURCEMANAGER_USER=root
    export YARN_NODEMANAGER_USER=root
    ```
- Apply these changes:
    ```bash
    source ~/.bashrc
    ```

### Starting Hadoop Services

- Start Hadoop services:
    ```bash
    start-all.sh
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
