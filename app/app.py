from pyspark.sql import SparkSession
import sys

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Pysparkexample") \
        .getOrCreate()
    try:
        df = spark.read.csv("hdfs://namenode:/user/jorge/data.csv")
        df.show()
        df.write.csv("hdfs://namenode:/user/jorge/mylittletest.csv")
        
    except Exception as e:
        print(str(e))
    finally:
        spark.stop()