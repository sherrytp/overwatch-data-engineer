# Set up Spark in the Cloud

## Installing Java

Download OpenJDK 11 or Oracle JDK 11 (It's important that the version is 11 - spark requires 8 or 11)

We'll use [OpenJDK](https://jdk.java.net/archive/)

Download it (e.g. to `~/spark`):

```
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```

Unpack it:

```bash
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
```

define `JAVA_HOME` and add it to `PATH`:

```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```

check that it works:

```bash
java --version
```

Output:

```
openjdk 11.0.2 2019-01-15
OpenJDK Runtime Environment 18.9 (build 11.0.2+9)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.2+9, mixed mode)
```

Remove the archive:

```bash
rm openjdk-11.0.2_linux-x64_bin.tar.gz
```

## Installing Spark

Download Spark. Use 3.3.2 version:

```bash
wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
```

Unpack:

```bash
tar xzfv spark-3.3.2-bin-hadoop3.tgz
```

Remove the archive:

```bash
rm spark-3.3.2-bin-hadoop3.tgz
```

Add it to `PATH`:

```bash
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```

## Hadoop

Next, we need to have Hadoop binaries. 

We'll need Hadoop 3.2 which we'll get from [here](https://github.com/cdarlint/winutils/tree/master/hadoop-3.2.0).

Create a folder (`/c/tools/hadoop-3.2.0`) and put the files there 

```bash
HADOOP_VERSION="3.2.0"
PREFIX="https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-${HADOOP_VERSION}/bin/"

FILES="hadoop.dll hadoop.exp hadoop.lib hadoop.pdb libwinutils.lib winutils.exe winutils.pdb"

for FILE in ${FILES}; do
  wget "${PREFIX}/${FILE}"
done
```

Add it to `PATH`:

```bash
export HADOOP_HOME="/c/tools/hadoop-3.2.0"
export PATH="${HADOOP_HOME}/bin:${PATH}"
```

## Testing Spark

Execute `spark-shell` and run the following:

```scala
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

## PySpark

This document assumes you already have python.

To run PySpark, we first need to add it to `PYTHONPATH`:

```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"
```

Make sure that the version under `${SPARK_HOME}/python/lib/` matches the filename of py4j or you will
encounter `ModuleNotFoundError: No module named 'py4j'` while executing `import pyspark`.

For example, if the file under `${SPARK_HOME}/python/lib/` is `py4j-0.10.9.3-src.zip`, then the
`export PYTHONPATH` statement above should be changed to

```bash
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.3-src.zip:$PYTHONPATH"
```

## Download and Set up gsutil

I used official guide from [Google gsutil](https://cloud.google.com/storage/docs/gsutil_install#deb) for a Linux Ubuntu setup. 

#### Prerequisites

Before you install the gcloud CLI, make sure that your operating system meets the following requirements:

* It is an Ubuntu release that hasn't reached end-of-life or a Debian stable release that hasn't reached end-of-life. 

* It has recently updated its packages:

    `sudo apt-get update`

* It has `apt-transport-https` and `curl` installed

#### Installation

1. Import the Google Cloud public key. 

    ```
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
    ```
2. Update and echo the key. 
    ```
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    ```
3. Update and intall the gcloud CLI: 
    ```
    sudo apt-get update && sudo apt-get install google-cloud-cli
    ```
4. (Optional) Install any of the following additional components. 

5. Run `gcloud init` to get started. 

6. (Optional) *Downgrading* gcloud CLI versions: 
    ```
    sudo apt-get update && sudo apt-get install google-cloud-cli=123.0.0-0
    ```


## Conecting Spark to Google Cloud Storage

* Download the jar for connecting to GCS to any location (e.g. the `lib` folder):

```bash
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar lib/gcs-connector-hadoop3-2.2.5.jar
```
* Uploading data to GCS. 
```bash
cd data/
gsutil -m cp -r pq/ gs://<bucket-name>/pq
```

* The option ```-m``` makes that all cpus are used
	* Make sure to authenticate gcloud via cli first:
		* ```export GOOGLE_APPLICATION_CREDENTIALS=<service-account-key>.json```
		* ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS```


--------
- if I can download data from GCS directly, and work with spark. 
- partition to separte files, use `tree data` to check the structure of the data folder. 
- write a schema like `05_taxi_schema`
- !!!! Important:



## Setting up a Dataproc Cluster

* Create a cluster in Google cloud
* Dataproc is a service from Google cloud
* Go to Goole cloud console and sear for "Dataproc"
* When you run it for the first time, make sure the DataProc API is enabled in your account
* Then click on "CREATE CLUSTER"
	* Cluster Name: `owl-analysis-bucket`
	* Choose a region (same as the bucket has): us-west1	
	* Choose a cluster type. Ususally you would choose "standard": 1 master, multiple workers, for our case single node is enough
	* Choose optional components: "Jupyter-Notebook", "Docker"
	* "CREATE" the cluster, creating a new VM
	* Go to the cluster and click on it, there you find a buttom "SUBMIT JOB"
	* Click on it, choose "Job type": PySpark
	* Next, the main python file has to be selected, for that our script needs to be uploaded. We can use the already created bucket for that, so don't configure the spark job as we did locally. 
	* In the terminal go to the folder where the script is stored and copy the pyspark job script to the bucket:  
	```gsutil cp <filename> gs://<bucket-name>/<location>/<filename>``` 
	
		(```gsutil cp spark_local_spark_cluster.py gs://de-spark-frauke/code/spark_local_spark_cluster.py```)

	* Then choose as "Main python script": 
	```
	gs://<bucket-name>/<location>/<filename>
	```
	* We have to specify `Arguments` using the data bucket instead of `data`, and just copy as separate lines: 
	```bash
	--input_green=gs://<bucket-name>/pq/green/2020/*
	--input_yellow=gs://<bucket-name>/<parquet-data-folder>/*
	--output=gs://<bucket-name>/report-2020
	```
	* Click "SUBMIT" job

	* we can also use the Google Cloud SDK or the REST API from documentation: https://cloud.google.com/dataproc/docs/guides/submit-job#dataproc-submit-job-gcloud
	* Add `Dataproc Adminitrator` to the service account for running permission before running this: 
	```
	gcloud dataproc jobs submit pyspark \
	--cluster=<custername> \
	--region=us-west1 \
	--jars=gs://spark-lib/bigqueryspark-bigquery-latest_2.12.jar \ 
	gs://<bucket-name>/<location>/<filename> \
	-- \
	--input_=gs://<bucket-name>/pq/green/2020/* \
    --input_yellow=gs://<bucket-name>/pq/yellow/2020/* \
    --output=gs://<bucket-name>/report
	```


## Read Spark Locally As DataFrames

* Save data to BigQuery
	```python
	df_result.write.format('bigquery') \ 
		.option('table', output) \ 
		.save()
	```
* Upload local files to GCS
	```python
	client = storage.Client("<client_name>")
	bucket_name = "owl-match-stats"
	bucket = client.get_bucket(bucket_name)
	blob = bucket.blob("owl_match.csv")
	blob.upload_from_string(csv_string, content_type='text/csv')
	```
* Read csv file:
	```
	df = spark.read\
		.option("header", "true") \
		.parquet('fhvhv_tripdata_2021-01.csv')
	```
	* Spark doesn't try to infer types, but reads everything as strings
	* Save the first 100 rows: ```head -n 101 fhvhv_tripdata_2021-01.csv > head.csv``` and read this file with pandas to check the types. Here also the timetamps are read as integers, the rest id ok
	* use ```spark.createDataFrame(df_pandas).show()``` to convert a pandas dataframe to a spark dataframe, then types are not all strings any more
	* Use the output of ```spark.createDataFrame(df_pandas).schema``` to define the types
	* use this schema to read the data in spark
* Now save data to parquet
* We now have one big file, this is not good in spark, so we will break it into multiple files - which are called **partitions** in spark
* ```df.repartition(24)```: This is a lazy command, it is only applied, when we actually do something
* ```df.write.parquet('fhvhv/2021/01')``` (this takes a while)  
* Read the created parquet files: ```spark.read.parquet("fhvhv/2021/01")```
