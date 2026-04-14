
# Import required libraries
import pandas as pd
import numpy as np


# STEP 1: Load CSV file

file_path = "data/trends_clean.csv"

try:
    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    exit()


# STEP 2: Explore data

print("
First 5 rows:")
print(df.head())

print("
Shape of DataFrame:", df.shape)

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("
Average score   :", avg_score)
print("Average comments:", avg_comments)

# STEP 3: NumPy Analysis
print("
--- NumPy Stats ---")

scores = df["score"].values

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)

print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
print(f"
Most stories in: {top_category} ({category_counts.max()} stories)")

# Most commented story
most_commented = df.loc[df["num_comments"].idxmax()]
print(f'
Most commented story: "{most_commented["title"]}" — {most_commented["num_comments"]} comments')

# STEP 4: Add new columns
# Engagement = comments per score
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score > average
df["is_popular"] = df["score"] > avg_score

# STEP 5: Save updated CSV

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"
Saved to {output_file}")

