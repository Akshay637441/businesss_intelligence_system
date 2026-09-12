import sqlite3
from pyspark.sql import SparkSession


# ============================================================
# SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("LoadBusinessAspectsToSQLite")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# PATHS
# ============================================================

HDFS_PATH = (
    "hdfs://localhost:9000/"
    "yelp/processed/business_aspects"
)

DB_PATH = "data/business_insights.db"


# ============================================================
# READ ASPECT DATA FROM HDFS
# ============================================================

print("Reading category-specific aspect data from HDFS...")

aspect_df = spark.read.parquet(HDFS_PATH)


print(
    f"HDFS records found: {aspect_df.count()}"
)


# ============================================================
# CONVERT TO LOCAL ROWS
# ============================================================

aspect_rows = (
    aspect_df
    .select(
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
    .collect()
)


print(
    f"Records collected: {len(aspect_rows)}"
)


# ============================================================
# CONNECT TO SQLITE
# ============================================================

print("Connecting to SQLite database...")

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()


# ============================================================
# CREATE TABLE IF NOT EXISTS
# ============================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS business_aspects (

        business_id TEXT,

        business_category TEXT,

        aspect TEXT,

        aspect_mentions INTEGER,

        positive_mentions INTEGER,

        neutral_mentions INTEGER,

        negative_mentions INTEGER,

        positive_percentage REAL,

        neutral_percentage REAL,

        negative_percentage REAL
    )
    """
)


# ============================================================
# REMOVE OLD ASPECT DATA
# ============================================================

print("Removing old aspect records...")

cursor.execute(
    "DELETE FROM business_aspects"
)

connection.commit()


print(
    f"Old records removed: {cursor.rowcount}"
)


# ============================================================
# INSERT NEW DATA
# ============================================================

print("Inserting new category-specific aspect data...")


insert_query = """
INSERT INTO business_aspects (
    business_id,
    business_category,
    aspect,
    aspect_mentions,
    positive_mentions,
    neutral_mentions,
    negative_mentions,
    positive_percentage,
    neutral_percentage,
    negative_percentage
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


batch = []

for row in aspect_rows:

    batch.append(
        (
            row["business_id"],
            row["business_category"],
            row["aspect"],
            int(row["aspect_mentions"]),
            int(row["positive_mentions"]),
            int(row["neutral_mentions"]),
            int(row["negative_mentions"]),
            float(row["positive_percentage"]),
            float(row["neutral_percentage"]),
            float(row["negative_percentage"])
        )
    )


cursor.executemany(
    insert_query,
    batch
)

connection.commit()


# ============================================================
# VERIFY TOTAL RECORDS
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM business_aspects"
)

total_records = cursor.fetchone()[0]


print()
print("=" * 60)
print("DATABASE LOAD COMPLETE")
print("=" * 60)

print(
    f"Records inserted: {total_records}"
)


# ============================================================
# VERIFY CATEGORY COUNTS
# ============================================================

print()
print("Records by category:")

cursor.execute(
    """
    SELECT
        business_category,
        COUNT(*)
    FROM business_aspects
    GROUP BY business_category
    ORDER BY business_category
    """
)

for category, count in cursor.fetchall():

    print(
        f"{category}: {count}"
    )


# ============================================================
# VERIFY ASPECT COUNTS
# ============================================================

print()
print("Aspect counts:")

cursor.execute(
    """
    SELECT
        business_category,
        aspect,
        COUNT(*)
    FROM business_aspects
    GROUP BY
        business_category,
        aspect
    ORDER BY
        business_category,
        aspect
    """
)

for category, aspect, count in cursor.fetchall():

    print(
        f"{category} | {aspect}: {count}"
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

spark.stop()


print()
print("=" * 60)
print("SUCCESS")
print("=" * 60)