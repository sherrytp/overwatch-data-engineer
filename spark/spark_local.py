#!/usr/bin/env python
# coding: utf-8

import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from google.cloud import storage


parser = argparse.ArgumentParser()

parser.add_argument('--input_match', required=True, 
                    help='Input path for match data')
parser.add_argument('--input_map', required=True, 
                    help='Input path for map data')
parser.add_argument('--output', required=True, 
                    help='Output path for the result')
args = parser.parse_args()

input_match = args.input_match
input_map = args.input_map
output = args.output

pyspark.conf.set('temporaryGcsBucket', 'dataproc-temp-us-west1-961201277689-mjds6r5g')

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

df_match = spark.read.csv(input_match)
df_map = spark.read.csv(input_map)

# upload to BigQuery
df_match.coalesce(1) \
    .write.format('bigquery') \
    .option('table', output, mode='overwrite') \
    .save()

# Upload to GCS
df_map.coalesce(1) \
    .write.parquet(output, mode='overwrite')
