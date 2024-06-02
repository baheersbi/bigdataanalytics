# Set Up the Spark Environment
1. Download and install Java by visiting this [Link](https://www.java.com/en/download/)
2. Make sure that you have ```Python``` installed in your machine.

    1.1. Type Python Or py > Hit Enter If Python Is Installed it will show the version Details Otherwise It will Open Microsoft Store To Download From Microsoft Store
3. Install ```PySpark``` using ```pip``` (Python package manager):
    ```bash
    pip install pyspark
    ```
4. Once the installation is completed, you can start the PySpark shell by running the pyspark command:
    ```bash
    pyspark
    ```
5. The PySpark interactive shell will look something like this: 
    ```bash
    Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.1
      /_/

    Using Python version 3.11.6 (v3.11.6:8b6ee5ba3b, Oct  2 2023 11:18:21)
    Spark context Web UI available at http://172.20.10.4:4040
    Spark context available as 'sc' (master = local[*], app id = local-1717365160333).
    SparkSession available as 'spark'.      
    >>>
    ```