
    # Import required library
import pandas as pd

# STEP 1: Load JSON file
file_path = "data/trends_20260414.json"  

try:
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# STEP 2: Remove duplicates
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# STEP 3: Remove missing values
# Drop rows where important fields are missing
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# STEP 4: Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# STEP 5: Remove low quality stories
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# STEP 6: Clean text (whitespace)
df["title"] = df["title"].str.strip()

# STEP 7: Save cleaned CSV
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"
Saved {len(df)} rows to {output_file}")

# STEP 8: Summary (stories per category)
print("
Stories per category:")
print(df["category"].value_counts())
