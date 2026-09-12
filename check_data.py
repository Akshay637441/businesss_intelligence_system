import json
from collections import Counter

FILE_PATH = "data/raw/yelp_academic_dataset_business.json"

total_businesses = 0
category_counts = Counter()

print("Reading Yelp business dataset...")
print()

with open(FILE_PATH, "r", encoding="utf-8") as file:

    for line in file:
        business = json.loads(line)

        total_businesses += 1

        categories = business.get("categories")

        if categories:
            for category in categories.split(","):
                category = category.strip()
                category_counts[category] += 1

        # Display the first business
        if total_businesses == 1:
            print("First business record:")
            print(json.dumps(business, indent=4))
            print()
            print("-" * 60)
            print()

print(f"Total businesses: {total_businesses:,}")

print()
print("Our selected categories:")
print()

target_categories = [
    "Restaurants",
    "Grocery",
    "Health & Medical",
    "Auto Repair"
]

for category in target_categories:
    print(f"{category}: {category_counts[category]:,}")

print()
print("-" * 60)
print("Top 20 business categories:")
print("-" * 60)

for category, count in category_counts.most_common(20):
    print(f"{category:<35} {count:,}")