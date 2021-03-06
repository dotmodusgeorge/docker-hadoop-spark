docker build --rm -t bde/spark-app .

echo "Submitting Job with args: \"${@}\""
docker run --rm \
    --name my-spark-app \
    -e ENABLE_INIT_DAEMON=false \
    --env-file .run.env \
    --network docker-hadoop-spark_default \
    --link spark-master:spark-master \
    bde/spark-app