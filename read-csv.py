# Databricks notebook version
from pyspark.sql import SparkSession
import pandas as pd

# File path in DBFS
csv_path = "/FileStore/shared_uploads/your_data.csv"

# Read the CSV file
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Display the DataFrame
display(df)

# Print schema and sample data
print("Schema:")
df.printSchema()

print("\nFirst 20 rows:")
display(df.limit(20))
