from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    avg
)


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Trend Analysis") \
    .getOrCreate()


# --------------------------------------------------
# 2. HDFS Paths
# --------------------------------------------------

INPUT_PATH = (
    "hdfs://localhost:9000/yelp/raw/"
    "yelp_academic_dataset_review.json"
)

OUTPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/"
    "review_trends"
)


# --------------------------------------------------
# 3. Load Review Data
# --------------------------------------------------

print("Loading Yelp review data...")

review_df = spark.read.json(INPUT_PATH)

print(
    "Total reviews:",
    review_df.count()
)


# --------------------------------------------------
# 4. Convert Date
# --------------------------------------------------

from pyspark.sql.functions import (
    to_timestamp,
    year,
    month,
    date_format
)

review_df = review_df.withColumn(
    "review_date",
    to_timestamp(col("date"))
)

review_df = review_df.withColumn(
    "review_year",
    year(col("review_date"))
).withColumn(
    "review_month",
    month(col("review_date"))
).withColumn(
    "review_year_month",
    date_format(
        col("review_date"),
        "yyyy-MM"
    )
)


# --------------------------------------------------
# 5. Yearly Review Trend
# --------------------------------------------------

yearly_reviews = review_df.groupBy(
    "review_year"
).agg(
    count("review_id").alias("review_count"),
    avg("stars").alias("average_rating")
).orderBy(
    "review_year"
)


print("\nYearly Review Trend:")

yearly_reviews.show(
    truncate=False
)


# --------------------------------------------------
# 6. Monthly Review Trend
# --------------------------------------------------

monthly_reviews = review_df.groupBy(
    "review_year_month"
).agg(
    count("review_id").alias("review_count"),
    avg("stars").alias("average_rating")
).orderBy(
    "review_year_month"
)


print("\nMonthly Review Trend:")

monthly_reviews.show(
    20,
    truncate=False
)


# --------------------------------------------------
# 7. Save Yearly Trend
# --------------------------------------------------

yearly_reviews.write \
    .mode("overwrite") \
    .parquet(
        f"{OUTPUT_PATH}/yearly"
    )


# --------------------------------------------------
# 8. Save Monthly Trend
# --------------------------------------------------

monthly_reviews.write \
    .mode("overwrite") \
    .parquet(
        f"{OUTPUT_PATH}/monthly"
    )


print(
    "\nTrend analysis completed successfully."
)

print(
    "Output:",
    OUTPUT_PATH
)


# --------------------------------------------------
# 9. Stop Spark
# --------------------------------------------------

spark.stop()