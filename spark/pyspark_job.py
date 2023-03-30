from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, window, avg, max, min
from pyspark.sql.types import (DoubleType, StringType, StructField, StructType,
                               TimestampType)

WINDOW_DURATION = '10 seconds'
DELAY_DURATION = '2 seconds'

# Kafka settings
KAFKA_BOOTSTRAP_URL = "broker:29092"
KAFKA_TOPIC = "processed_messages"

# MongoDB settings
MONGODB_CONNECTION_URL = 'mongodb://paaiAdmin:paaiAdminPasswd%2123@mongo:27017/paai?authSource=paai&readPreference=primary'
MONGODB_DATABASE = 'paai'
MONGODB_COLLECTION = 'aggregated_messages'


# Create a Spark session
spark = SparkSession.builder \
    .appName('IoTDataProcessor') \
    .config("spark.mongodb.read.connection.uri", "mongodb://mongo:27017/paai.processed_messages?readPreference=primaryPreferred") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongo:27017/paai.processed_messages") \
    .getOrCreate()

# Define the schema for the Kafka messages
device_message_schema = StructType([
    StructField("timestamp", TimestampType()),
    StructField("device_id", StringType()),
    StructField("sensor", StringType()),
    StructField("value", DoubleType())
])

# Subscribe to topic 
kafka_df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_URL) \
  .option("subscribe", KAFKA_TOPIC) \
  .load() \
  .selectExpr("CAST(value AS STRING)") \
  .select(from_json("value", device_message_schema).alias("data")) \
  .select("data.*")


aggregated_df = kafka_df \
                .withWatermark("timestamp", DELAY_DURATION) \
                .groupBy(window("timestamp", windowDuration=WINDOW_DURATION,slideDuration=WINDOW_DURATION), "device_id") \
                .agg(avg("value").alias("avg"), max("value").alias("max"), min("value").alias("min"))

# Writing to MongoDB
aggregated_df.writeStream \
  .format("mongodb") \
  .option("checkpointLocation", "/tmp/pysparkmongo") \
  .option("forceDeleteTempCheckpointLocation", "true") \
  .option('spark.mongodb.connection.uri', MONGODB_CONNECTION_URL) \
  .option('spark.mongodb.database', MONGODB_DATABASE) \
  .option('spark.mongodb.collection', MONGODB_COLLECTION) \
  .outputMode("append") \
  .start()

spark.streams.awaitAnyTermination()
