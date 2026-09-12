import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Top Business Opportunities
# --------------------------------------------------

opportunity_data = {
    "location": [
        "Santa Barbara, CA",
        "Reno, NV",
        "New Orleans, LA",
        "Saint Petersburg, FL",
        "Sparks, NV"
    ],
    "category": [
        "Restaurant",
        "Restaurant",
        "Restaurant",
        "Restaurant",
        "Restaurant"
    ],
    "opportunity_score": [
        89.31,
        87.27,
        85.86,
        85.78,
        85.36
    ]
}

df = pd.DataFrame(opportunity_data)


plt.figure(figsize=(10, 5))

plt.barh(
    df["location"],
    df["opportunity_score"]
)

plt.xlabel("Opportunity Score")
plt.ylabel("Location")
plt.title("Top Business Opportunities")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "visualisations/top_business_opportunities.png",
    dpi=300
)

plt.show()

print(
    "Opportunity visualization saved successfully."
)