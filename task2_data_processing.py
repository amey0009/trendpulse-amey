# ============================================================
# Task 2 - Data Cleaning & CSV Export (TrendPulse)
# ============================================================

import pandas as pd
import os
import glob

# -----------------------------
# 1. LOAD JSON FILE
# Find the most recently created trends JSON in data/
# -----------------------------
files = glob.glob("data/trends_*.json")
if not files:
    raise FileNotFoundError("No JSON file found in data/ folder. Run Task 1 first.")

# Pick the latest file by name (YYYYMMDD suffix sorts correctly)
file = sorted(files)[-1]

df = pd.read_json(file)
print(f"Loaded {len(df)} stories from {file}")

# -----------------------------
# 2. REMOVE DUPLICATES
# Drop rows that share the same post_id — same story fetched twice
# -----------------------------
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# -----------------------------
# 3. REMOVE MISSING VALUES
# Only drop rows where post_id, title, or score is missing.
# num_comments (descendants) can be null on HackerNews for stories
# with zero comments — that is valid data, so we do NOT drop on it.
# -----------------------------
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# -----------------------------
# 4. FIX DATA TYPES
# Coerce score to numeric (handles edge cases), then cast to int.
# For num_comments, fill nulls with 0 first — a null descendants
# value simply means 0 comments, not bad data.
# -----------------------------
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# Fill null num_comments with 0 before converting — HackerNews
# returns null for descendants when a story has no comments yet.
df["num_comments"] = pd.to_numeric(
    df["num_comments"].fillna(0), errors="coerce"
).fillna(0)

# Drop only if score conversion failed (truly bad data)
df = df.dropna(subset=["score"])

df["score"]        = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# -----------------------------
# 5. STRIP WHITESPACE FROM TITLE
# Done after nulls are removed so .str accessor is safe
# -----------------------------
df["title"] = df["title"].astype(str).str.strip()

# -----------------------------
# 6. FILTER LOW-QUALITY DATA
# Remove stories with a score below 5 (spec requirement)
# -----------------------------
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# -----------------------------
# 7. FILL REMAINING MISSING CATEGORICAL COLUMNS
# author and category should always be present, but guard just in case
# -----------------------------
df["author"]   = df["author"].fillna("unknown")
df["category"] = df["category"].fillna("unknown")

# -----------------------------
# 8. SAVE CLEANED DATA AS CSV
# -----------------------------
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

# Print confirmation in the exact format the spec requires
print(f"Saved {len(df)} rows to {output_file}")

# -----------------------------
# 9. STORIES PER CATEGORY SUMMARY
# -----------------------------
print("\nStories per category:")
print(df["category"].value_counts().to_string())
