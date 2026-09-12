from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import (
    StringIndexer,
    OneHotEncoder,
    VectorAssembler
)
from pyspark.ml.classification import RandomForestClassifier


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Feature Engineering and ML") \
    .getOrCreate()


# --------------------------------------------------
# 2. HDFS Paths
# --------------------------------------------------

BUSINESS_INPUT = (
    "hdfs://localhost:9000/yelp/processed/business_analysis"
)

BUSINESS_MODEL_OUTPUT = (
    "hdfs://localhost:9000/yelp/models/"
    "business_health_random_forest"
)


# --------------------------------------------------
# 3. Load Business Analysis Data
# --------------------------------------------------

print("Loading business analysis data...")

business_analysis = spark.read.parquet(
    BUSINESS_INPUT
)

print(
    "Business records:",
    business_analysis.count()
)


# --------------------------------------------------
# 4. Select ML Features
# --------------------------------------------------

ml_data = business_analysis.select(
    "stars",
    "review_count",
    "is_open",
    "positive_percentage",
    "negative_percentage",
    "business_category",
    "health_status"
)


# --------------------------------------------------
# 5. Encode Business Category
# --------------------------------------------------

category_indexer = StringIndexer(
    inputCol="business_category",
    outputCol="category_index"
)

category_indexer_model = category_indexer.fit(
    ml_data
)

ml_data = category_indexer_model.transform(
    ml_data
)


encoder = OneHotEncoder(
    inputCol="category_index",
    outputCol="category_vector"
)

ml_data = encoder.fit(
    ml_data
).transform(ml_data)


# --------------------------------------------------
# 6. Assemble Features
# --------------------------------------------------

assembler = VectorAssembler(
    inputCols=[
        "stars",
        "review_count",
        "is_open",
        "positive_percentage",
        "negative_percentage",
        "category_vector"
    ],
    outputCol="features"
)

ml_data = assembler.transform(
    ml_data
)


# --------------------------------------------------
# 7. Encode Health Status
# --------------------------------------------------

label_indexer = StringIndexer(
    inputCol="health_status",
    outputCol="label"
)

label_indexer_model = label_indexer.fit(
    ml_data
)

ml_data = label_indexer_model.transform(
    ml_data
)


# --------------------------------------------------
# 8. Select Final ML Data
# --------------------------------------------------

final_ml_data = ml_data.select(
    "features",
    "label",
    "health_status"
)


# --------------------------------------------------
# 9. Split Training and Testing Data
# --------------------------------------------------

train_data, test_data = final_ml_data.randomSplit(
    [0.8, 0.2],
    seed=42
)

print(
    "Training records:",
    train_data.count()
)

print(
    "Testing records:",
    test_data.count()
)


# --------------------------------------------------
# 10. Train Random Forest
# --------------------------------------------------

rf = RandomForestClassifier(
    featuresCol="features",
    labelCol="label",
    numTrees=100,
    seed=42
)

print("Training Random Forest model...")

rf_model = rf.fit(
    train_data
)

print(
    "Business Health Random Forest trained successfully."
)


# --------------------------------------------------
# 11. Generate Predictions
# --------------------------------------------------

predictions = rf_model.transform(
    test_data
)


# --------------------------------------------------
# 12. Calculate Accuracy
# --------------------------------------------------

correct_predictions = predictions.filter(
    col("prediction") == col("label")
).count()

total_predictions = predictions.count()

accuracy = (
    correct_predictions /
    total_predictions
)

print(
    "Business Health Model Accuracy:",
    accuracy
)

print(
    "Business Health Model Accuracy (%):",
    accuracy * 100
)


# --------------------------------------------------
# 13. Display Predictions
# --------------------------------------------------

predictions.select(
    "health_status",
    "label",
    "prediction"
).show(10)


# --------------------------------------------------
# 14. Save Random Forest Model
# --------------------------------------------------

print("Saving Business Health model...")

rf_model.write \
    .overwrite() \
    .save(BUSINESS_MODEL_OUTPUT)


print(
    "Business Health model saved successfully."
)

print(
    "Model:",
    BUSINESS_MODEL_OUTPUT
)


# --------------------------------------------------
# 15. Stop Spark
# --------------------------------------------------

spark.stop()