from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    when
)


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Sentiment Analysis") \
    .getOrCreate()


# --------------------------------------------------
# 2. HDFS Paths
# --------------------------------------------------

INPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/business_analysis"
)

OUTPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/"
    "business_sentiment_analysis"
)


# --------------------------------------------------
# 3. Load Business Analysis Data
# --------------------------------------------------

print("Loading business analysis data...")

business_analysis = spark.read.parquet(INPUT_PATH)

print(
    "Total businesses:",
    business_analysis.count()
)


# --------------------------------------------------
# 4. Calculate Overall Sentiment Statistics
# --------------------------------------------------

total_businesses = business_analysis.count()

average_positive = business_analysis.select(
    "positive_percentage"
).groupBy().avg().collect()[0][0]

average_negative = business_analysis.select(
    "negative_percentage"
).groupBy().avg().collect()[0][0]


print("\nOverall Business Sentiment:")

print(
    "Average Positive Percentage:",
    average_positive
)

print(
    "Average Negative Percentage:",
    average_negative
)


# --------------------------------------------------
# 5. Identify Businesses with High Negative Sentiment
# --------------------------------------------------

high_negative_businesses = business_analysis.filter(
    col("negative_percentage") >= 50
).select(
    "business_id",
    "name",
    "business_category",
    "stars",
    "total_reviews",
    "positive_percentage",
    "negative_percentage",
    "business_health_score",
    "risk_score",
    "risk_status"
).orderBy(
    col("negative_percentage").desc()
)


print("\nBusinesses with 50% or More Negative Reviews:")

high_negative_businesses.show(
    20,
    truncate=False
)


# --------------------------------------------------
# 6. Sentiment by Business Category
# --------------------------------------------------

category_sentiment = business_analysis.groupBy(
    "business_category"
).agg(
    count("business_id").alias("business_count"),
    (
        sum("positive_reviews") /
        sum("total_reviews") * 100
    ).alias("positive_percentage"),
    (
        sum("negative_reviews") /
        sum("total_reviews") * 100
    ).alias("negative_percentage")
).orderBy(
    col("negative_percentage").desc()
)


print("\nSentiment by Business Category:")

category_sentiment.show(
    truncate=False
)


# --------------------------------------------------
# 7. Save Sentiment Analysis
# --------------------------------------------------

business_analysis.write \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH)


print(
    "\nSentiment analysis completed successfully."
)

print(
    "Output:",
    OUTPUT_PATH
)


# --------------------------------------------------
# 8. Stop Spark
# --------------------------------------------------

spark.stop()