import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

credentials_location = '~/.google/credentials/google_credentials.json'
gcp_bucket = 'owl-match-stats'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)

sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

df_match = spark.read.csv(f'gs://{gcp_bucket}/phs_2021_1.csv')
df_map = spark.read.csv(f'gs://{gcp_bucket}/match_map_stats.csv')

df_joined = df_match.join(df_map, df_match.esports_match_id == df_map.match_id)

df_modified = df_joined.withColumn(
    'match_id', df_joined['match_id'].cast('string')).withColumn(
        'stat_amount', df_joined['stat_amout'].cast('float')
    ) #.withColumn("timestamp", F.from_unixtime(test_json_df["timestamp"]/1000)).select(F.explode("data").alias("data"), "timestamp")

df_dmg = spark.sql("""
    SELECT start_time, esports_match_id, map_name, 
            play_name, team_name, hero_name, stat_amount
    FROM modified
    WHERE stat_name = "Hero Damage Done"
""")

df_dmg.coalesce(1) \
    .write.format('bigquery') \
    .option('table', output, mode='overwrite') \
    .save()
