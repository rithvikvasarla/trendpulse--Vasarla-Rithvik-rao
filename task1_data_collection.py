 
# Importing required libraries
import requests
import time
import json
import os
from datetime import datetime

# This ensures our output file has a place to go
if not os.path.exists("data"):
    os.makedirs("data")

# STEP 1: Define API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header
headers = {"User-Agent": "TrendPulse/1.0"}

# STEP 2: Define categories + keywords
# We will match story titles with these keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# STEP 3: Function to assign category
# This checks if any keyword is present in title
def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category
    
    # If nothing matches, it assigns a default category (to avoid losing stories)
    return "technology"

# STEP 4: Fetch top story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]  # Only first 500
    print("Top story IDs fetched successfully")
except Exception as e:
    print("Error fetching top stories:", e)
    story_ids = []

# STEP 5: Fetch stories category-wise
all_stories = []
# Loop through each category
for category in categories.keys():
    count = 0  # To track 25 stories per category

    for story_id in story_ids:
        if count >= 25:
            break  # It Stops when we reach 25

        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            story = res.json()

            # Skips if story is invalid or no title
            if not story or "title" not in story:
                continue

            # Checks category using title
            assigned_category = get_category(story["title"])

            # Only store if category matches current loop
            if assigned_category == category or assigned_category is not None:
                data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                all_stories.append(data)
                count += 1

        except Exception as e:
            print(f"Failed to fetch story {story_id}")
            continue  # Continue even if one request fails

    # Wait 2 seconds AFTER each category
    print(f"{category} stories collected:", count)
    time.sleep(2)

# STEP 6: Save data to JSON file
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(filename, "w") as f:
    json.dump(all_stories, f, indent=4)
# Final output
print(f"
Collected {len(all_stories)} stories.")
print(f"Saved to {filename}")
