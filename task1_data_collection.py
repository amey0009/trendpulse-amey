

# ============================================================
# TrendPulse - Task 1: Fetch Data from HackerNews API
# ============================================================
# What this script does:
#   1. Fetches the top 500 story IDs from HackerNews
#   2. Grabs details for each story (title, score, comments, etc.)
#   3. Assigns each story a category based on keywords in its title
#   4. Saves everything to a JSON file inside a 'data/' folder
# ============================================================

import requests   # For making HTTP calls to the API
import json       # For saving data in JSON format
import os         # For creating folders
import time       # For adding delays between requests
from datetime import datetime  # For recording when data was collected

# ── STEP 1: Define categories and their matching keywords ───────────────────
# We check if any of these words appear in the story title (case-insensitive)
CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}

# Max stories we want per category (as per requirement)
MAX_PER_CATEGORY = 25

# Header to identify our app when calling the API
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Base URLs for the HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL       = "https://hacker-news.firebaseio.com/v0/item/{id}.json"


# ── STEP 2: Helper function to assign a category ────────────────────────────
def assign_category(title):
    """
    Looks at the story title and returns the first matching category.
    If no keyword matches, returns None (we skip these stories).
    """
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return None


# ── STEP 3: Fetch the list of top story IDs ─────────────────────────────────
print("Fetching top story IDs from HackerNews...")

try:
    response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    all_ids = response.json()[:500]   # Only first 500 IDs (as required)
    print(f"Got {len(all_ids)} story IDs.")
except Exception as e:
    print(f"Failed to fetch story IDs: {e}")
    exit()


# ── STEP 4: Fetch story details and collect by category ─────────────────────
# This dictionary will hold our collected stories grouped by category
collected = {category: [] for category in CATEGORIES}

print("\nFetching story details and sorting into categories...")

# Loop category-wise
for category in CATEGORIES:
    print(f"\nCollecting {category} stories...")

    for story_id in all_ids:
        if len(collected[category]) >= MAX_PER_CATEGORY:
            break

        try:
            url = STORY_URL.format(id=story_id)
            story_response = requests.get(url, headers=HEADERS, timeout=10)
            story_response.raise_for_status()
            story = story_response.json()

            if not story or story.get("type") != "story":
                continue

            title = story.get("title", "")
            detected_category = assign_category(title)

            # Only collect if it matches current category
            if detected_category != category:
                continue

            story_data = {
                "post_id":      story.get("id"),
                "title":        story.get("title", ""),
                "category":     category,
                "score":        story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author":       story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            collected[category].append(story_data)

        except Exception as e:
            print(f"  Warning: Could not fetch story ID {story_id}: {e}")
            continue

    # Sleep once per category loop as required
    time.sleep(2)


# ── STEP 5: Print category counts ────────────────────────────
print("\nCategory counts:")
for category in CATEGORIES:
    count = len(collected[category])
    print(f"  {category}: {count} stories collected")


# ── STEP 6: Flatten all stories into one list ───────────────────────────────
all_stories = []
for category_stories in collected.values():
    all_stories.extend(category_stories)


# ── STEP 7: Save to JSON file ────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)

today = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_stories, f, indent=2, ensure_ascii=False) # indent=2 formats JSON for readability
# ensure_ascii=False keeps text in UTF-8 (no unicode escape sequences)

# ── STEP 8: Print final summary ──────────────────────────────────────────────
print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")

print("\nBreakdown by category:")
for category, stories in collected.items():
    print(f"  {category}: {len(stories)} stories")

