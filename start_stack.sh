#!/bin/bash

docker-compose -f docker-compose-hive.yml up -d namenode hive-metastore-postgresql
docker-compose -f docker-compose-hive.yml up -d datanode hive-metastore
docker-compose -f docker-compose-hive.yml up -d hive-server
docker-compose -f docker-compose-hive.yml up -d spark-master spark-worker-1 hue
docker-compose -f docker-compose-hive.yml up -d presto

my_ip=`ip route get 1|awk '{print $NF;exit}'`
echo "Namenode: http://localhost:50070"
echo "Datanode: http://localhost:50075"
echo "Spark-master: http://localhost:8080"
echo "Hive Server: jdbc:hive2://localhost:10000"
echo "PrestoDB: jdbc:presto://localhost:8089/default"
echo "Hue (HDFS Filebrowser): http://localhost:8088/home"
