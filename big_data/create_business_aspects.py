from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    lower,
    when,
    lit,
    sum as spark_sum,
    round as spark_round
)


# ============================================================
# SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("YelpCategorySpecificAspectAnalysis")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# HDFS PATHS
# ============================================================

BUSINESS_PATH = (
    "hdfs://localhost:9000/"
    "yelp/raw/yelp_academic_dataset_business.json"
)

REVIEW_PATH = (
    "hdfs://localhost:9000/"
    "yelp/raw/yelp_academic_dataset_review.json"
)

OUTPUT_PATH = (
    "hdfs://localhost:9000/"
    "yelp/processed/business_aspects"
)


# ============================================================
# READ BUSINESS DATA
# ============================================================

print("Reading business data...")

business_df = (
    spark.read
    .json(BUSINESS_PATH)
    .select(
        "business_id",
        "categories"
    )
)


# ============================================================
# CLASSIFY BUSINESS CATEGORY
# ============================================================

print("Classifying business categories...")

business_df = business_df.withColumn(
    "business_category",

    when(
        lower(col("categories"))
        .contains("restaurant"),
        "Restaurant"
    )

    .when(
        lower(col("categories"))
        .contains("grocery"),
        "Grocery"
    )

    .when(
        lower(col("categories")).contains("health & medical")
        |
        lower(col("categories")).contains("medical center")
        |
        lower(col("categories")).contains("doctors")
        |
        lower(col("categories")).contains("dentists")
        |
        lower(col("categories")).contains("hospital"),
        "Healthcare"
    )

    .when(
        lower(col("categories"))
        .contains("auto repair"),
        "Auto Repair"
    )

    .otherwise("Other")
)


# ============================================================
# KEEP ONLY FOUR FOCUS INDUSTRIES
# ============================================================

business_df = business_df.filter(
    col("business_category").isin(
        "Restaurant",
        "Grocery",
        "Healthcare",
        "Auto Repair"
    )
)


# ============================================================
# READ REVIEW DATA
# ============================================================

print("Reading review data...")

review_df = (
    spark.read
    .json(REVIEW_PATH)
    .select(
        "business_id",
        "text",
        "stars"
    )
)


# ============================================================
# JOIN BUSINESS + REVIEW
# ============================================================

print("Joining reviews with businesses...")

df = (
    review_df
    .join(
        business_df,
        on="business_id",
        how="inner"
    )
)


# ============================================================
# PREPARE REVIEW TEXT
# ============================================================

df = df.withColumn(
    "review_text",
    lower(
        col("text")
    )
)


# ============================================================
# STAR-BASED SENTIMENT
# ============================================================

df = df.withColumn(
    "sentiment",

    when(
        col("stars") >= 4,
        "Positive"
    )

    .when(
        col("stars") == 3,
        "Neutral"
    )

    .otherwise("Negative")
)


# ============================================================
# CATEGORY-SPECIFIC ASPECT CONDITIONS
# ============================================================

# ------------------------------------------------------------
# RESTAURANT
# ------------------------------------------------------------

restaurant_aspects = {

    "Food": [
        "food",
        "meal",
        "dish",
        "taste",
        "flavor",
        "menu",
        "pizza",
        "burger",
        "dessert",
        "drink",
        "drinks",
        "coffee"
    ],

    "Service": [
        "service",
        "waiter",
        "waitress",
        "server",
        "customer service",
        "order",
        "wait",
        "slow service"
    ],

    "Staff": [
        "staff",
        "employee",
        "employees",
        "manager",
        "worker",
        "crew",
        "host",
        "bartender"
    ],

    "Price": [
        "price",
        "prices",
        "expensive",
        "cheap",
        "cost",
        "value",
        "worth",
        "overpriced"
    ],

    "Quality": [
        "quality",
        "fresh",
        "clean",
        "professional",
        "excellent",
        "poor quality"
    ],

    "Ambience": [
        "ambience",
        "ambiance",
        "atmosphere",
        "environment",
        "decor",
        "decoration",
        "music",
        "seating",
        "noise"
    ]
}


# ------------------------------------------------------------
# GROCERY
# ------------------------------------------------------------

grocery_aspects = {

    "Product Quality": [
        "product",
        "products",
        "quality",
        "fresh",
        "freshness",
        "produce",
        "meat",
        "vegetables",
        "fruit",
        "groceries",
        "expired",
        "expiration"
    ],

    "Price": [
        "price",
        "prices",
        "expensive",
        "cheap",
        "cost",
        "value",
        "deal",
        "discount",
        "sale",
        "overpriced"
    ],

    "Staff": [
        "staff",
        "employee",
        "employees",
        "manager",
        "worker",
        "cashier"
    ],

    "Service": [
        "service",
        "customer service",
        "checkout",
        "cashier",
        "help",
        "helpful",
        "slow"
    ],

    "Variety": [
        "variety",
        "selection",
        "options",
        "choices",
        "assortment",
        "brands",
        "products"
    ],

    "Cleanliness": [
        "clean",
        "cleanliness",
        "dirty",
        "messy",
        "store",
        "aisle",
        "sanitary"
    ]
}


# ------------------------------------------------------------
# HEALTHCARE
# ------------------------------------------------------------

healthcare_aspects = {

    "Doctors": [
        "doctor",
        "doctors",
        "physician",
        "specialist",
        "surgeon",
        "dentist",
        "nurse",
        "nurses"
    ],

    "Staff": [
        "staff",
        "employee",
        "employees",
        "receptionist",
        "nurse",
        "manager",
        "worker"
    ],

    "Service": [
        "service",
        "customer service",
        "care",
        "patient care",
        "treatment",
        "support"
    ],

    "Wait Time": [
        "wait",
        "waiting",
        "waited",
        "wait time",
        "waiting time",
        "appointment",
        "delay",
        "delayed",
        "long wait"
    ],

    "Quality of Care": [
        "quality",
        "care",
        "treatment",
        "professional",
        "diagnosis",
        "medical care",
        "healthcare",
        "excellent",
        "poor care"
    ],

    "Cleanliness": [
        "clean",
        "cleanliness",
        "dirty",
        "sanitary",
        "hygiene",
        "hospital",
        "clinic",
        "room"
    ]
}


# ------------------------------------------------------------
# AUTO REPAIR
# ------------------------------------------------------------

auto_repair_aspects = {

    "Service": [
        "service",
        "customer service",
        "repair service",
        "maintenance",
        "mechanic",
        "mechanics"
    ],

    "Staff": [
        "staff",
        "employee",
        "employees",
        "manager",
        "mechanic",
        "technician",
        "worker"
    ],

    "Price": [
        "price",
        "prices",
        "expensive",
        "cheap",
        "cost",
        "value",
        "worth",
        "overpriced",
        "estimate"
    ],

    "Repair Quality": [
        "repair",
        "repairs",
        "quality",
        "fixed",
        "fix",
        "work",
        "job",
        "professional",
        "damage"
    ],

    "Wait Time": [
        "wait",
        "waiting",
        "waited",
        "wait time",
        "waiting time",
        "delay",
        "delayed",
        "appointment"
    ],

    "Parts": [
        "part",
        "parts",
        "replacement",
        "component",
        "tire",
        "tires",
        "battery",
        "brake",
        "brakes",
        "oil"
    ]
}


# ============================================================
# CREATE ASPECT DATA
# ============================================================

aspect_dataframes = []


# ============================================================
# RESTAURANT ASPECTS
# ============================================================

for aspect_name, keywords in restaurant_aspects.items():

    condition = None

    for keyword in keywords:

        keyword_condition = (
            col("review_text").contains(keyword)
        )

        if condition is None:
            condition = keyword_condition
        else:
            condition = condition | keyword_condition


    aspect_df = (
        df
        .filter(
            (col("business_category") == "Restaurant")
            &
            condition
        )
        .withColumn(
            "aspect",
            lit(aspect_name)
        )
    )

    aspect_dataframes.append(
        aspect_df
    )


# ============================================================
# GROCERY ASPECTS
# ============================================================

for aspect_name, keywords in grocery_aspects.items():

    condition = None

    for keyword in keywords:

        keyword_condition = (
            col("review_text").contains(keyword)
        )

        if condition is None:
            condition = keyword_condition
        else:
            condition = condition | keyword_condition


    aspect_df = (
        df
        .filter(
            (col("business_category") == "Grocery")
            &
            condition
        )
        .withColumn(
            "aspect",
            lit(aspect_name)
        )
    )

    aspect_dataframes.append(
        aspect_df
    )


# ============================================================
# HEALTHCARE ASPECTS
# ============================================================

for aspect_name, keywords in healthcare_aspects.items():

    condition = None

    for keyword in keywords:

        keyword_condition = (
            col("review_text").contains(keyword)
        )

        if condition is None:
            condition = keyword_condition
        else:
            condition = condition | keyword_condition


    aspect_df = (
        df
        .filter(
            (col("business_category") == "Healthcare")
            &
            condition
        )
        .withColumn(
            "aspect",
            lit(aspect_name)
        )
    )

    aspect_dataframes.append(
        aspect_df
    )


# ============================================================
# AUTO REPAIR ASPECTS
# ============================================================

for aspect_name, keywords in auto_repair_aspects.items():

    condition = None

    for keyword in keywords:

        keyword_condition = (
            col("review_text").contains(keyword)
        )

        if condition is None:
            condition = keyword_condition
        else:
            condition = condition | keyword_condition


    aspect_df = (
        df
        .filter(
            (col("business_category") == "Auto Repair")
            &
            condition
        )
        .withColumn(
            "aspect",
            lit(aspect_name)
        )
    )

    aspect_dataframes.append(
        aspect_df
    )


# ============================================================
# COMBINE ALL ASPECT DATA
# ============================================================

print("Combining category-specific aspects...")

combined_aspects = aspect_dataframes[0]

for aspect_df in aspect_dataframes[1:]:

    combined_aspects = combined_aspects.unionByName(
        aspect_df
    )


# ============================================================
# BUSINESS-LEVEL SUMMARY
# ============================================================

print(
    "Creating business-level aspect summary..."
)


aspect_summary = (
    combined_aspects
    .groupBy(
        "business_id",
        "business_category",
        "aspect"
    )
    .agg(

        spark_sum(
            when(
                col("sentiment") == "Positive",
                1
            ).otherwise(0)
        ).alias(
            "positive_mentions"
        ),

        spark_sum(
            when(
                col("sentiment") == "Neutral",
                1
            ).otherwise(0)
        ).alias(
            "neutral_mentions"
        ),

        spark_sum(
            when(
                col("sentiment") == "Negative",
                1
            ).otherwise(0)
        ).alias(
            "negative_mentions"
        )

    )
)


# ============================================================
# TOTAL MENTIONS
# ============================================================

aspect_summary = aspect_summary.withColumn(
    "aspect_mentions",

    col("positive_mentions")
    +
    col("neutral_mentions")
    +
    col("negative_mentions")
)


# ============================================================
# PERCENTAGES
# ============================================================

aspect_summary = aspect_summary.withColumn(
    "positive_percentage",

    spark_round(
        (
            col("positive_mentions")
            /
            col("aspect_mentions")
        ) * 100,
        2
    )
)


aspect_summary = aspect_summary.withColumn(
    "neutral_percentage",

    spark_round(
        (
            col("neutral_mentions")
            /
            col("aspect_mentions")
        ) * 100,
        2
    )
)


aspect_summary = aspect_summary.withColumn(
    "negative_percentage",

    spark_round(
        (
            col("negative_mentions")
            /
            col("aspect_mentions")
        ) * 100,
        2
    )
)


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

aspect_summary = aspect_summary.select(
    "business_id",
    "business_category",
    "aspect",
    "aspect_mentions",
    "positive_mentions",
    "neutral_mentions",
    "negative_mentions",
    "positive_percentage",
    "neutral_percentage",
    "negative_percentage"
)


# ============================================================
# WRITE TO HDFS
# ============================================================

print(
    "Writing business aspect data to HDFS..."
)


(
    aspect_summary
    .write
    .mode("overwrite")
    .parquet(OUTPUT_PATH)
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 55)
print("CATEGORY-SPECIFIC ASPECT ANALYSIS COMPLETE")
print("=" * 55)


record_count = aspect_summary.count()


print(
    f"Business-aspect records: {record_count}"
)


print()
print("Records by business category:")


(
    aspect_summary
    .groupBy("business_category")
    .count()
    .orderBy("business_category")
    .show(
        20,
        truncate=False
    )
)


print()
print("Aspect distribution:")


(
    aspect_summary
    .groupBy(
        "business_category",
        "aspect"
    )
    .count()
    .orderBy(
        "business_category",
        "aspect"
    )
    .show(
        100,
        truncate=False
    )
)


print()
print("Sample records:")


(
    aspect_summary
    .orderBy("business_category", "aspect")
    .show(
        20,
        truncate=False
    )
)


print()
print(
    f"Output location: {OUTPUT_PATH}"
)


print()
print("=" * 55)
print("SUCCESS")
print("=" * 55)


spark.stop()