# ============================================================
# Task 1 - Fetch Data from HackerNews API (TrendPulse)
# ============================================================

import requests
import json
import os
import time
from datetime import datetime

# -----------------------------
# Category keyword mapping
# -----------------------------
CATEGORIES = {
    "technology":    ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

HEADERS = {"User-Agent": "TrendPulse/1.0"}

TOP_URL  = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# -----------------------------
# Function: assign category
# -----------------------------
def get_category(title):
    """Check the title against each category's keywords and return the first match."""
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title_lower:
                return category
    return None  # no matching category found


# -----------------------------
# Step 1: Fetch top 500 IDs (with error handling)
# -----------------------------
print("Fetching top story IDs...")
try:
    response = requests.get(TOP_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    story_ids = response.json()[:500]
except Exception as e:
    print(f"Failed to fetch top story IDs: {e}")
    story_ids = []

# -----------------------------
# Storage: list for all stories + per-category counters
# -----------------------------
final_stories = []
category_count = {c: 0 for c in CATEGORIES}

# -----------------------------
# Step 2: Loop over categories — one sleep per category
# This is the correct structure: outer loop = category,
# inner loop = story IDs, sleep happens once per category.
# -----------------------------
for category in CATEGORIES:

    print(f"Collecting stories for category: {category}")

    for sid in story_ids:
        # Stop collecting for this category once we have 25 stories
        if category_count[category] >= 25:
            break

        try:
            res = requests.get(ITEM_URL.format(sid), headers=HEADERS, timeout=10)
            data = res.json()

            # Skip non-story items or items with no data
            if not data or data.get("type") != "story":
                continue

            title = (data.get("title") or "").strip()

            # Only add this story if it belongs to the current category
            if get_category(title) == category:
                story = {
                    "post_id":      data.get("id"),
                    "title":        title,
                    "category":     category,
                    "score":        data.get("score", 0),
                    "num_comments": data.get("descendants", 0),  # null means 0 comments
                    "author":       data.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                final_stories.append(story)
                category_count[category] += 1

        except Exception as e:
            # Don't crash — just skip this story and log the issue
            print(f"Skipping story {sid}: {e}")
            continue

    # ONE sleep per category loop (not per individual story fetch)
    time.sleep(2)

# -----------------------------
# Step 3: Save JSON output
# -----------------------------
os.makedirs("data", exist_ok=True)

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(final_stories, f, indent=2, ensure_ascii=False)

# Print the required confirmation message
print(f"Collected {len(final_stories)} stories. Saved to {filename}")
