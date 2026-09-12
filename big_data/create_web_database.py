from pyspark.sql import SparkSession
import sqlite3
import os


# ============================================
# CONFIGURATION
# ============================================

HDFS_PATH = "hdfs://localhost:9000/yelp/processed/business_analysis"

DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "business_insights.db")


# ============================================
# CREATE DATABASE DIRECTORY
# ============================================

os.makedirs(DATABASE_DIR, exist_ok=True)


# ============================================
# START SPARK
# ============================================

spark = (
    SparkSession.builder
    .appName("CreateWebDatabase")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================
# READ PROCESSED BUSINESS DATA
# ============================================

print("\nReading business analysis data from HDFS...")

df = spark.read.parquet(HDFS_PATH)


# ============================================
# SELECT ONLY WEB-REQUIRED COLUMNS
# ============================================

web_df = df.select(
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
    "rating_score",
    "review_score",
    "open_score",
    "review_score_normalized",
    "business_health_score",
    "health_status",
    "total_reviews",
    "positive_reviews",
    "neutral_reviews",
    "negative_reviews",
    "positive_percentage",
    "negative_percentage",
    "risk_score",
    "risk_status"
)


# ============================================
# CONVERT TO PANDAS
# ============================================

print("Converting data for the web database...")

pdf = web_df.toPandas()

print(f"Businesses loaded: {len(pdf):,}")


# ============================================
# CREATE SQLITE DATABASE
# ============================================

print("\nCreating SQLite database...")

connection = sqlite3.connect(DATABASE_PATH)


# Write data
pdf.to_sql(
    "businesses",
    connection,
    if_exists="replace",
    index=False
)


# ============================================
# CREATE INDEXES
# ============================================

print("Creating database indexes...")

cursor = connection.cursor()

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_business_id
    ON businesses(business_id)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_business_name
    ON businesses(name)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_business_category
    ON businesses(business_category)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_business_city
    ON businesses(city)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_business_state
    ON businesses(state)
""")


connection.commit()


# ============================================
# VERIFY
# ============================================

cursor.execute("SELECT COUNT(*) FROM businesses")

count = cursor.fetchone()[0]

print(f"\nDatabase verification:")
print(f"Businesses in database: {count:,}")
print(f"Database location: {DATABASE_PATH}")


connection.close()

spark.stop()

print("\nWeb database creation completed successfully.")