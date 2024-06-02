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
   /__ / .__/\_,_/_/ /_/\_\   version 3.2.0
      /_/

    Using Python version 3.8.12 (default, Oct 12 2021 05:06:12)
    Spark context Web UI available at http://192.168.1.10:4040
    Spark context available as 'sc' (master = local[*], app id = local-1643040323444)
    SparkSession available as 'spark'

    >>>
    ```