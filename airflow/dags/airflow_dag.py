import os
import json
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator, DataprocSubmitJobOperator
from google.cloud import storage

# Environment variables
BUCKET = os.environ.get("GCP_GCS_BUCKET", "owl-match-stats")
PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'owl_data')
PYSPARK_URI = f'gs://{BUCKET}/scripts/owl_pyspark_job.py'
gcs_path = 'owl_raw.csv'  # Assuming CSV format
mode = 'update'  # Example mode, specify as needed

# Dataproc cluster configuration
CLUSTER_CONFIG = {
    "project_id": PROJECT_ID,
    "zone": "us-west1-b",
    "master_disk_size": 500,
    "num_masters": 1,
    "num_workers": 0,  # single node mode
    "idle_delete_ttl": 900,  # idle time before deleting cluster
    "init_actions_uris": [f'gs://{BUCKET}/scripts/pip-script.sh'],
    "metadata": {'PIP_PACKAGES': 'spark'}
}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False
}

def get_data():
    url = 'https://www.kaggle.com/datasets/sherrytp/overwatch-league-stats-lab/'
    data = pd.read_csv(url+'phs_2021_1.csv')
    return data


def upload_to_gcs(response_data):
    timestamp = response_data["timestamp"]
    dt_object = datetime.fromtimestamp(timestamp/1000)
    created_date = dt_object
    storage_client = storage.Client()
    bucket_name = "owl-match-stats"
    bucket = storage_client.get_bucket(bucket_name)
    destination_blob_name = f'{created_date}.csv'
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json.dumps(response_data))


def ingest_data():
    response_data = get_data()
    upload_to_gcs(response_data)

dag = DAG(
    'owl_data_pipeline',
    default_args=default_args,
    description='Fetch and process OWL data from Kaggle',
    schedule_interval=timedelta(days=1)
)

upload_to_gcs_task = PythonOperator(
    task_id='ingest_data',
    python_callable=ingest_data, 
    dag=dag
)

create_cluster = DataprocCreateClusterOperator(
    task_id='create_dataproc_cluster',
    project_id=PROJECT_ID,
    cluster_config=CLUSTER_CONFIG,
    region='us-west1',
    dag=dag
)

pyspark_job = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": 'de-spark-cluster'},
    "pyspark_job": {
        "main_python_file_uri": PYSPARK_URI,
        "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
        "properties": {
            "spark.jars.packages": "com.johnsnowlabs.nlp:spark-nlp_2.12:3.4.3"
        },
        "args": [
            f"--input=gs://{BUCKET}/{gcs_path}",
            f"--dataset={BIGQUERY_DATASET}",
            "--mode=update"
        ]
    }
}

submit_pyspark_job = DataprocSubmitJobOperator(
    task_id='submit_pyspark_job',
    job=pyspark_job,
    region='us-west1',
    dag=dag
)

# Define task dependencies
upload_to_gcs_task >> create_cluster >> submit_pyspark_job