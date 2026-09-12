import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Sentiment Distribution Visualization
# --------------------------------------------------

sentiment_data = {
    "sentiment": [
        "Negative",
        "Neutral",
        "Positive"
    ],
    "review_count": [
        1613801,
        691934,
        4684545
    ]
}

df = pd.DataFrame(sentiment_data)


plt.figure(figsize=(8, 5))

plt.bar(
    df["sentiment"],
    df["review_count"]
)

plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.title("Yelp Review Sentiment Distribution")

plt.tight_layout()

plt.savefig(
    "visualisations/sentiment_distribution.png",
    dpi=300
)

plt.show()

print(
    "Sentiment distribution visualization saved successfully."
)