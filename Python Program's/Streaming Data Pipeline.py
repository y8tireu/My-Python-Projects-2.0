#Server
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    data = {"event": "temperature", "value": 25.5}
    producer.send("test_topic", data)
    print(f"Sent: {data}")
    time.sleep(1)
#Consumer
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, FloatType

spark = SparkSession.builder.appName("KafkaSparkStream").getOrCreate()

# Define schema for incoming data
schema = StructType().add("event", StringType()).add("value", FloatType())

# Read from Kafka
kafka_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test_topic") \
    .load()

# Deserialize and parse Kafka data
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING) as json") \
    .selectExpr("json_extract(json, '$.event') as event", "json_extract(json, '$.value') as value")

query = parsed_stream.writeStream.outputMode("append").format("console").start()
query.awaitTermination()
