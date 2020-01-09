docker build --rm -t bde/spark-app .
docker run --rm --name my-spark-app -e ENABLE_INIT_DAEMON=false --network docker-hadoop-spark_default --link spark-master:spark-master bde/spark-app > logs.txt