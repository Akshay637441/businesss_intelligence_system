from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    to_timestamp,
    year,
    month,
    date_format,
    length,
    lower,
    regexp_replace,
    trim,
    explode,
    count,
    sum
)
from pyspark.sql.functions import expr
from pyspark.ml.feature import Tokenizer, StopWordsRemover


# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Yelp Review NLP Processing") \
    .getOrCreate()


# --------------------------------------------------
# 2. HDFS Paths
# --------------------------------------------------

INPUT_PATH = (
    "hdfs://localhost:9000/yelp/raw/"
    "yelp_academic_dataset_review.json"
)

OUTPUT_BASE = "hdfs://localhost:9000/yelp/processed"


# --------------------------------------------------
# 3. Load Review Dataset
# --------------------------------------------------

print("Loading Yelp review data...")

review_df = spark.read.json(INPUT_PATH)

print("Total reviews:", review_df.count())


# --------------------------------------------------
# 4. Clean Review Data
# --------------------------------------------------

review_clean = review_df.filter(
    col("business_id").isNotNull()
    & col("review_id").isNotNull()
    & col("stars").isNotNull()
    & col("text").isNotNull()
    & col("date").isNotNull()
)


# --------------------------------------------------
# 5. Convert Review Date
# --------------------------------------------------

review_clean = review_clean.withColumn(
    "review_date",
    to_timestamp(col("date"))
)

review_clean = review_clean.withColumn(
    "review_year",
    year(col("review_date"))
).withColumn(
    "review_month",
    month(col("review_date"))
).withColumn(
    "review_year_month",
    date_format(col("review_date"), "yyyy-MM")
)


# --------------------------------------------------
# 6. Create Sentiment Labels from Ratings
# --------------------------------------------------

review_clean = review_clean.withColumn(
    "sentiment_label",
    when(col("stars") >= 4, "Positive")
    .when(col("stars") == 3, "Neutral")
    .otherwise("Negative")
)


# --------------------------------------------------
# 7. Display Sentiment Distribution
# --------------------------------------------------

print("\nSentiment Distribution:")

review_clean.groupBy(
    "sentiment_label"
).count().show()


# --------------------------------------------------
# 8. Prepare Reviews for NLP
# --------------------------------------------------

review_nlp = review_clean.filter(
    length(col("text")) >= 10
)


# --------------------------------------------------
# 9. Clean Review Text
# --------------------------------------------------

review_nlp = review_nlp.withColumn(
    "clean_text",
    lower(col("text"))
)

review_nlp = review_nlp.withColumn(
    "clean_text",
    regexp_replace(
        col("clean_text"),
        r"http\S+|www\S+",
        ""
    )
)

review_nlp = review_nlp.withColumn(
    "clean_text",
    regexp_replace(
        col("clean_text"),
        r"[^a-zA-Z\s]",
        " "
    )
)

review_nlp = review_nlp.withColumn(
    "clean_text",
    regexp_replace(
        col("clean_text"),
        r"\s+",
        " "
    )
)

review_nlp = review_nlp.withColumn(
    "clean_text",
    trim(col("clean_text"))
)


# --------------------------------------------------
# 10. Tokenization
# --------------------------------------------------

tokenizer = Tokenizer(
    inputCol="clean_text",
    outputCol="words"
)

review_tokenized = tokenizer.transform(review_nlp)


# --------------------------------------------------
# 11. Remove Stop Words
# --------------------------------------------------

remover = StopWordsRemover(
    inputCol="words",
    outputCol="filtered_words"
)

review_filtered = remover.transform(review_tokenized)


# --------------------------------------------------
# 12. Custom Stop Words
# --------------------------------------------------

review_filtered = review_filtered.withColumn(
    "filtered_words",
    expr("""
        filter(
            filtered_words,
            x -> NOT array_contains(
                array(
                    've',
                    'm',
                    'got',
                    'get',
                    'go',
                    'one',
                    'us'
                ),
                x
            )
        )
    """)
)


# --------------------------------------------------
# 13. Word Frequency
# --------------------------------------------------

word_counts = review_filtered.select(
    explode(col("filtered_words")).alias("word")
).groupBy(
    "word"
).count().orderBy(
    col("count").desc()
)


print("\nTop 30 Words:")

word_counts.show(30, truncate=False)


# --------------------------------------------------
# 14. Save Word Frequency
# --------------------------------------------------

word_counts.write \
    .mode("overwrite") \
    .parquet(
        f"{OUTPUT_BASE}/word_counts"
    )


# --------------------------------------------------
# 15. Save Clean NLP Data
# --------------------------------------------------

review_filtered.select(
    "review_id",
    "business_id",
    "stars",
    "sentiment_label",
    "review_date",
    "review_year",
    "review_month",
    "review_year_month",
    "clean_text",
    "filtered_words"
).write \
    .mode("overwrite") \
    .parquet(
        f"{OUTPUT_BASE}/review_nlp"
    )


print("\nReview and NLP processing completed successfully.")
print("Word counts:", f"{OUTPUT_BASE}/word_counts")
print("NLP data:", f"{OUTPUT_BASE}/review_nlp")


# --------------------------------------------------
# 16. Stop Spark
# --------------------------------------------------

spark.stop()