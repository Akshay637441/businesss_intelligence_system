import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Yearly Review Trend Visualization
# --------------------------------------------------

trend_data = {
    "year": [
        2005, 2006, 2007, 2008, 2009,
        2010, 2011, 2012, 2013, 2014,
        2015, 2016, 2017, 2018, 2019,
        2020, 2021, 2022
    ],
    "review_count": [
        854,
        3853,
        15363,
        48226,
        74387,
        138587,
        230813,
        286570,
        383950,
        522275,
        688415,
        758882,
        820048,
        906362,
        907284,
        554557,
        618189,
        31665
    ]
}

df = pd.DataFrame(trend_data)


plt.figure(figsize=(10, 5))

plt.plot(
    df["year"],
    df["review_count"],
    marker="o"
)

plt.xlabel("Year")
plt.ylabel("Number of Reviews")
plt.title("Yelp Reviews by Year")

plt.xticks(df["year"], rotation=45)

plt.tight_layout()

plt.savefig(
    "visualisations/yearly_review_trend.png",
    dpi=300
)

plt.show()

print(
    "Yearly review trend visualization saved successfully."
)