from pyspark.sql import SparkSession
import sys

"""
For reading and writing files to HDFS
    df = spark.read.csv("hdfs://namenode:/path_to_file/data.csv")
    df.write.csv("hdfs://namenode:/path_to_file/mylittletest.csv")
"""
if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Pysparkexample") \
        .getOrCreate()
    try:
        print("Hello!")
        
    except Exception as e:
        print(str(e))
    finally:
        spark.stop()