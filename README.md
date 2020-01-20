# Docker Hadoop PySpark

## Initial Setup

```bash
git clone https://github.com/dotmodusgeorge/docker-hadoop-spark

cd docker-hadoop-spark

./start_stack.sh
```

When all of the containers are up, you can create a virtualenv in the root of the directory. 

```bash
virtualenv env

# or

python3 -m venv env
```

Activate the environment

```bash
source ./env/bin/activate
```

## HDFS

To add source files to HDFS, you find the HUE UI on http://localhost:8088. After creating your user, if you receive a Django error, just navigate to http://localhost:8088/home. 

On the top left you'll see `File Browser`. This will open the HDFS storage view and will allow you to manage your files on HDFS.

Ideally, create a user named `root`.

## Running a PySpark App

Script arguments can be set in the .run.env file. Just append your arguments to the end of the line. For example:

```bash
SPARK_APPLICATION_ARGS=user/root raw/simple/ stage/simple/ simple
```

To run your App in spark, run:

```bash
cd ./app
./run.sh
```