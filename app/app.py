from pyspark.sql import SparkSession, catalog
from pyspark.sql import functions as f
from datetime import datetime, timedelta
from time import time
from pathlib import Path
import sys
from tqdm import tqdm
import argparse

def get_raw_files(sc, host, path):
    URI = sc._gateway.jvm.java.net.URI
    Path = sc._gateway.jvm.org.apache.hadoop.fs.Path
    FileSystem = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
    Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration
    fs = FileSystem.get(URI(host), Configuration())
    status = fs.listStatus(Path(path))
    res = []
    for fileStatus in status:
        res.append(str(fileStatus.getPath()))
    return res

def table_exists(spark, name):
    table_list_raw=spark.catalog.listTables()
    table_list = [table.name for table in table_list_raw]
    return name in table_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hdfs_base_path")
    parser.add_argument("raw_file_dir")
    parser.add_argument("stage_file")
    parser.add_argument("table_name")
    args = parser.parse_args()

    hdfs_node = "hdfs://namenode"
    raw_dir = F"{hdfs_node}/{args.hdfs_base_path}/{args.raw_file_dir}"
    orc_path = F"{hdfs_node}/{args.hdfs_base_path}/{args.stage_file}"
    table_name = args.table_name

    spark = SparkSession \
        .builder \
        .appName("Pysparkexample") \
        .config('hive.metastore.uris', 'thrift://hive-metastore:9083') \
        .enableHiveSupport() \
        .getOrCreate()

    logger = spark.sparkContext._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

    try:
        raw_files = get_raw_files(spark.sparkContext, hdfs_node, raw_dir)
        s = time()
        print(F'-> Starting job at {datetime.now()} and loading {len(raw_files)} files')
        with tqdm(total=len(raw_files)) as pbar:
            i = 0
            for index, file in enumerate(raw_files):
                edr_timestamp = int(datetime.now().timestamp())
                raw_filename = Path(file)
                input_file = F"{raw_filename.stem}{raw_filename.suffix}"
                df = spark.read.option("header", "true").csv(file)
                df = df.withColumn("edr", f.lit(edr_timestamp))
                df = df.withColumn("inputfile", f.lit(input_file))
                df.write.partitionBy(['inputfile', 'edr']).mode('append').orc(orc_path)
                if not table_exists(spark, table_name):
                    spark.catalog.createTable(
                        table_name, 
                        path=orc_path, 
                        source="org.apache.spark.sql.hive.orc.OrcFileFormat",
                    )
                # Reload table partitions
                spark.sql("MSCK REPAIR TABLE {}".format(table_name))
                pbar.update(1)
                i = i+1

    except Exception as e:
        print(str(e))
    finally:
        spark.stop()
        e = time()
        print(F'-> Job ended at {datetime.now()}')
        print(F'-> Loaded {len(raw_files)} in {e - s} seconds')
