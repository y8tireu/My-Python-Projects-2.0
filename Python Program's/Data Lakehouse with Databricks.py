from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Databricks Lakehouse").getOrCreate()

# Read data from raw files
raw_df = spark.read.option("header", "true").csv("/mnt/raw_data/")

# Transformation
transformed_df = raw_df.filter(raw_df["value"] > 10)

# Write to Delta Lake
transformed_df.write.format("delta").mode("overwrite").save("/mnt/lakehouse/processed_data")

print("Data Lakehouse Process Completed")
