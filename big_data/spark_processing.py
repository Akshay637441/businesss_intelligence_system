from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    lower,
    when,
    log1p,
    max as spark_max
)


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Business Processing") \
    .getOrCreate()


# --------------------------------------------------
# 2. HDFS Paths
# --------------------------------------------------

INPUT_PATH = "hdfs://localhost:9000/yelp/raw/yelp_academic_dataset_business.json"

OUTPUT_PATH = "hdfs://localhost:9000/yelp/processed/business_health"


# --------------------------------------------------
# 3. Load Business Dataset
# --------------------------------------------------

print("Loading Yelp business data...")

business_df = spark.read.json(INPUT_PATH)

print("Total businesses:", business_df.count())


# --------------------------------------------------
# 4. Classify Businesses
# --------------------------------------------------

business_df = business_df.withColumn(
    "business_category",
    when(
        lower(col("categories")).contains("restaurant"),
        "Restaurant"
    )
    .when(
        lower(col("categories")).contains("grocery"),
        "Grocery"
    )
    .when(
        lower(col("categories")).contains("health & medical") |
        lower(col("categories")).contains("medical center") |
        lower(col("categories")).contains("doctors") |
        lower(col("categories")).contains("dentists") |
        lower(col("categories")).contains("hospital"),
        "Healthcare"
    )
    .when(
        lower(col("categories")).contains("auto repair"),
        "Auto Repair"
    )
    .otherwise("Other")
)


# --------------------------------------------------
# 5. Handle Missing Categories
# --------------------------------------------------

business_df = business_df.fillna({
    "categories": "Unknown"
})


# --------------------------------------------------
# 6. Select Required Columns
# --------------------------------------------------

business_clean = business_df.select(
    "business_id",
    "name",
    "business_category",
    "categories",
    "address",
    "city",
    "state",
    "postal_code",
    "latitude",
    "longitude",
    "stars",
    "review_count",
    "is_open",
    "attributes",
    "hours"
)


# --------------------------------------------------
# 7. Calculate Business Health Features
# --------------------------------------------------

business_features = business_clean.withColumn(
    "rating_score",
    (col("stars") / 5.0) * 100
).withColumn(
    "review_score",
    log1p(col("review_count"))
).withColumn(
    "open_score",
    when(col("is_open") == 1, 100).otherwise(0)
)


# --------------------------------------------------
# 8. Normalize Review Score
# --------------------------------------------------

max_review_score = business_features.agg(
    spark_max("review_score").alias("max_review_score")
).collect()[0]["max_review_score"]


business_health = business_features.withColumn(
    "review_score_normalized",
    (col("review_score") / max_review_score) * 100
)


# --------------------------------------------------
# 9. Calculate Business Health Score
# --------------------------------------------------

business_health = business_health.withColumn(
    "business_health_score",
    (col("rating_score") * 0.50)
    + (col("review_score_normalized") * 0.30)
    + (col("open_score") * 0.20)
)


# --------------------------------------------------
# 10. Assign Health Status
# --------------------------------------------------

business_health = business_health.withColumn(
    "health_status",
    when(
        col("business_health_score") >= 70,
        "Healthy"
    )
    .when(
        col("business_health_score") >= 50,
        "Moderate"
    )
    .otherwise("At Risk")
)


# --------------------------------------------------
# 11. Display Results
# --------------------------------------------------

print("\nBusiness Health Summary:")

business_health.groupBy(
    "health_status"
).count().show()


# --------------------------------------------------
# 12. Save Processed Data to HDFS
# --------------------------------------------------

print("Saving business health data to HDFS...")

business_health.write \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH)


print("Business processing completed successfully.")
print("Output:", OUTPUT_PATH)


# --------------------------------------------------
# 13. Stop Spark
# --------------------------------------------------

spark.stop()