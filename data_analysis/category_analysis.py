from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Category Analysis") \
    .getOrCreate()


# --------------------------------------------------
# 2. Load Business Analysis Data
# --------------------------------------------------

INPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/business_analysis"
)

OUTPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/category_summary"
)

print("Loading business analysis data...")

business_analysis = spark.read.parquet(INPUT_PATH)

print(
    "Total businesses:",
    business_analysis.count()
)


# --------------------------------------------------
# 3. Category Summary
# --------------------------------------------------

category_summary = business_analysis.groupBy(
    "business_category"
).agg(
    count("business_id").alias("business_count"),
    avg("stars").alias("average_rating")
).orderBy(
    "business_count",
    ascending=False
)


# --------------------------------------------------
# 4. Display Results
# --------------------------------------------------

print("\nBusiness Category Summary:")

category_summary.show(
    truncate=False
)


# --------------------------------------------------
# 5. Save Results
# --------------------------------------------------

category_summary.write \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH)


print(
    "Category analysis completed successfully."
)

print(
    "Output:",
    OUTPUT_PATH
)


# --------------------------------------------------
# 6. Stop Spark
# --------------------------------------------------

spark.stop()