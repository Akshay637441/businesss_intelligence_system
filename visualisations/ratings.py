import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Rating Distribution Visualization
# --------------------------------------------------

rating_data = {
    "stars": [1, 2, 3, 4, 5],
    "review_count": [
        1069561,
        544240,
        691934,
        1452918,
        3231627
    ]
}

df = pd.DataFrame(rating_data)


plt.figure(figsize=(8, 5))

plt.bar(
    df["stars"],
    df["review_count"]
)

plt.xlabel("Star Rating")
plt.ylabel("Number of Reviews")
plt.title("Yelp Review Rating Distribution")

plt.xticks([1, 2, 3, 4, 5])

plt.tight_layout()

plt.savefig(
    "visualisations/rating_distribution.png",
    dpi=300
)

plt.show()

print(
    "Rating distribution visualization saved successfully."
)