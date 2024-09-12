# Apache Hive
This section continues our exploration of Apache Hadoop configuration and usage, now shifting to Apache Hive. We’ll cover Hive’s setup, configuration, demonstrating how it simplifies querying large datasets in Hadoop. Additionally, we’ll show you how to access and use Hive within IntelliJ IDEA, streamlining your development workflow and running Hive queries directly from the IDE.
> [!IMPORTANT]
> Ensure the Docker container is running and the necessary ports are exposed. See https://github.com/baheersbi/bigdataanalytics/tree/main/hadoop

1. Log into the running Docker container
```bash
# Windows Users
docker exec -it myhadoop bash

# Mac Users
docker exec -it bigtools bash 
```
2. Make sure Thrift Server for Hive (Port ```10000```) and Hive Metastore (Port ```9083```) are running. 
> [!NOTE]
> You would need to use ```netstat``` and often it's not pre-installed in some Linux distributions, so you would need to install it:
> ```bash
> apt update && apt install -y net-tools
> ```
```bash
netstat -tuln
```
This should show Hive listening on ```0.0.0.0:10000``` and ```0.0.0.0:9083```. If these ports are not open, you may need to start the Hive Metastore manually:
```bash
hive --service metastore &
```
and the Hive Thrift server:
```bash
hive --service hiveserver2 &
```
3. 
## Connecting IntelliJ to Hive

