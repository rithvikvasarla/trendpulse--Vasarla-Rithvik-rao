
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# STEP 1: Load data and setup
# -------------------------------
file_path = "data/trends_analysed.csv"

try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully")
except Exception as e:
    print("Error loading file:", e)
    exit()

# Create outputs folder if not exists
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# -------------------------------
# STEP 2: Chart 1 - Top 10 Stories by Score
# -------------------------------
# Get top 10 stories
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles (more than 50 characters)
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Save before showing
plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# -------------------------------
# STEP 3: Chart 2 - Stories per Category
# -------------------------------
category_counts = df["category"].value_counts()

plt.figure()
category_counts.plot(kind="bar")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.show()

# -------------------------------
# STEP 4: Chart 3 - Score vs Comments
# -------------------------------
plt.figure()

# Separate popular and non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.show()

# -------------------------------
# BONUS: Dashboard (All charts together)
# -------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")

# Chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")

# Chart 3 in dashboard
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")

fig.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")
plt.show()

print("All charts saved in outputs/ folder")
