# Docker Hadoop Pypsark

```bash
git clone https://github.com/dotmodusgeorge/docker-hadoop-spark

cd docker-hadoop-spark

./start-hadoop-spark.sh
```

When all of the containers are up, you can open the `app` folder and create your pyspark app in there.

To run your App in spark, run:

```bash
cd ./app
./run.sh
```

To add files to HDFS, you find view on http://localhost:8088. After creating your user, if you receive a Django error, just navigate to http://localhost:8088/home. 

On the top left you'll see `File Browser`. This will open the HDFS storage view and you can manage your files like that. 