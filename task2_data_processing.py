
# ============================================================
# TrendPulse - Task 2: Clean & Process Data (JSON → CSV)
# ============================================================
# What this script does:
#   1. Loads the JSON file created by Task 1
#   2. Cleans the data (removes duplicates, fills missing values, etc.)
#   3. Saves the cleaned data as a CSV file
# ============================================================

import json       # To read the JSON file from Task 1
import csv        # To write the output CSV file
import os         # To handle file paths
import glob       # To find the JSON file by pattern
from datetime import datetime

# ── STEP 1: Find and load the JSON file from Task 1 ─────────────────────────
print("Looking for Task 1 JSON file...")

# Find any file matching data/trends_*.json
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("ERROR: No JSON file found in 'data/' folder. Run Task 1 first!")
    exit()

# If multiple files exist, use the most recent one
json_file = sorted(json_files)[-1]
print(f"Found: {json_file}")

with open(json_file, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

print(f"Loaded {len(raw_data)} raw stories.")


# ── STEP 2: Clean the data ──────────────────────────────────────────────────
print("\nCleaning data...")

cleaned_data = []
seen_ids = set()   # Track post IDs to remove duplicates

for story in raw_data:

    # ── Remove duplicates: skip if we've already seen this post_id ──────────
    post_id = story.get("post_id")
    if post_id in seen_ids:
        continue  # Skip duplicate
    seen_ids.add(post_id)

    # ── Skip stories with no title ───────────────────────────────────────────
    title = story.get("title", "").strip()
    if not title:
        continue

    # ── Fill in missing numeric values with 0 ───────────────────────────────
    score = story.get("score", 0)
    if score is None or score == "":
        score = 0

    num_comments = story.get("num_comments", 0)
    if num_comments is None or num_comments == "":
        num_comments = 0

    # ── Fill in missing text values with a default ───────────────────────────
    author = story.get("author", "unknown").strip()
    if not author:
        author = "unknown"

    category = story.get("category", "").strip()

    collected_at = story.get("collected_at", "")
    if not collected_at:
        collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Ensure score and num_comments are integers, not strings ─────────────
    try:
        score = int(score)
    except (ValueError, TypeError):
        score = 0

    try:
        num_comments = int(num_comments)
    except (ValueError, TypeError):
        num_comments = 0

    # ── Build the cleaned record ─────────────────────────────────────────────
    cleaned_story = {
        "post_id":      post_id,
        "title":        title,
        "category":     category,
        "score":        score,
        "num_comments": num_comments,
        "author":       author,
        "collected_at": collected_at,
    }

    cleaned_data.append(cleaned_story)

print(f"After cleaning: {len(cleaned_data)} stories remain.")
print(f"Removed {len(raw_data) - len(cleaned_data)} duplicates/invalid entries.")


# ── STEP 3: Save cleaned data to CSV ────────────────────────────────────────
os.makedirs("data", exist_ok=True)

today = datetime.now().strftime("%Y%m%d")
csv_filename = f"data/trends_cleaned_{today}.csv"

# Define the column order for the CSV
fieldnames = ["post_id", "title", "category", "score", "num_comments", "author", "collected_at"]

with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()       # Write the column names as the first row
    writer.writerows(cleaned_data)  # Write all story rows

print(f"\nCleaned CSV saved to: {csv_filename}")
print(f"Total stories in CSV: {len(cleaned_data)}")

# ── STEP 4: Quick preview — show first 3 rows ────────────────────────────────
print("\nPreview (first 3 stories):")
for story in cleaned_data[:3]:
    print(f"  [{story['category'].upper()}] {story['title'][:60]}... | Score: {story['score']}")