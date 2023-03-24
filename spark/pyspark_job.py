from pyspark.sql import SparkSession
from datetime import datetime, date
from pyspark.sql import Row
import time

# Create a Spark session
spark = SparkSession.builder \
    .appName('IoTDataProcessor') \
    .config("spark.mongodb.read.connection.uri", "mongodb://mongo:27017/paai.processed_messages?readPreference=primaryPreferred") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongo:27017/paai.processed_messages") \
    .getOrCreate()

# Subscribe to topic 
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "65.108.162.34:9392") \
  .option("subscribe", "spark_test") \
  .load()
# Producing to topic
# query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
#         .writeStream \
#         .format("kafka") \
#         .option("kafka.bootstrap.servers", "65.108.162.34:9392") \
#         .option("topic", "spark_test_sink") \
#         .option("checkpointLocation", "/tmp/checkpoints") \
#         .start()

# Writing to MongoDB

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")\
    .writeStream \
    .format("mongodb") \
    .option("checkpointLocation", "/tmp/pysparkmongo") \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .option('spark.mongodb.connection.uri', 'mongodb://paaiAdmin:paaiAdminPasswd%2123@mongo:27017/paai?authSource=paai&readPreference=primary') \
    .option('spark.mongodb.database', 'paai') \
    .option('spark.mongodb.collection', 'processed_messages') \
    .outputMode("append") \
    .start()


spark.streams.awaitAnyTermination()
