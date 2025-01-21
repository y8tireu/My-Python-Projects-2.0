from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("ETL Pipeline") \
    .getOrCreate()

# Extract: Load raw data
data = spark.read.csv("data/raw_data.csv", header=True, inferSchema=True)

# Transform: Clean and process data
data_cleaned = data.dropna()  # Example transformation: remove null values

# Load: Save to processed directory
data_cleaned.write.parquet("data/processed_data.parquet", mode="overwrite")

print("ETL Pipeline completed!")
