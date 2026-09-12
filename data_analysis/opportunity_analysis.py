from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    avg,
    sum,
    log1p,
    max as spark_max
)


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Business Opportunity Analysis") \
    .getOrCreate()


# --------------------------------------------------
# 2. HDFS Paths
# --------------------------------------------------

INPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/"
    "business_decline"
)

OUTPUT_PATH = (
    "hdfs://localhost:9000/yelp/processed/"
    "opportunity_analysis"
)


# --------------------------------------------------
# 3. Load Business Decline Data
# --------------------------------------------------

print("Loading business decline data...")

business_decline = spark.read.parquet(INPUT_PATH)

print(
    "Total businesses:",
    business_decline.count()
)


# --------------------------------------------------
# 4. City and Category Analysis
# --------------------------------------------------

city_category_analysis = business_decline.groupBy(
    "city",
    "state",
    "business_category"
).agg(
    count("business_id").alias("business_count"),
    avg("stars").alias("average_rating"),
    sum("review_count").alias("total_reviews"),
    avg("business_health_score").alias(
        "average_health_score"
    ),
    avg("negative_percentage").alias(
        "average_negative_percentage"
    )
)


# --------------------------------------------------
# 5. Calculate Demand Score
# --------------------------------------------------

city_category_analysis = city_category_analysis.withColumn(
    "demand_score",
    log1p(col("total_reviews"))
)


# --------------------------------------------------
# 6. Find Maximum Values for Normalization
# --------------------------------------------------

max_values = city_category_analysis.agg(
    spark_max("demand_score").alias("max_demand"),
    spark_max("business_count").alias("max_competition")
).collect()[0]

max_demand = max_values["max_demand"]
max_competition = max_values["max_competition"]


# --------------------------------------------------
# 7. Normalize Demand and Competition
# --------------------------------------------------

city_category_analysis = city_category_analysis.withColumn(
    "demand_normalized",
    (col("demand_score") / max_demand) * 100
).withColumn(
    "competition_normalized",
    (col("business_count") / max_competition) * 100
)


# --------------------------------------------------
# 8. Calculate Opportunity Score
# --------------------------------------------------

city_category_analysis = city_category_analysis.withColumn(
    "opportunity_score",
    (col("demand_normalized") * 0.60)
    + (
        (100 - col("competition_normalized"))
        * 0.40
    )
)


# --------------------------------------------------
# 9. Display Top Opportunities
# --------------------------------------------------

top_opportunities = city_category_analysis.orderBy(
    col("opportunity_score").desc()
)


print("\nTop Business Opportunities:")

top_opportunities.select(
    "city",
    "state",
    "business_category",
    "business_count",
    "average_rating",
    "total_reviews",
    "average_health_score",
    "average_negative_percentage",
    "opportunity_score"
).show(
    20,
    truncate=False
)


# --------------------------------------------------
# 10. Save Opportunity Analysis
# --------------------------------------------------

top_opportunities.write \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH)


print(
    "\nOpportunity analysis completed successfully."
)

print(
    "Output:",
    OUTPUT_PATH
)


# --------------------------------------------------
# 11. Stop Spark
# --------------------------------------------------

spark.stop()