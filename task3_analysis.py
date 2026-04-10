# ============================================================
# Task 3 - Analysis with Pandas & NumPy (TrendPulse)
# ============================================================

import pandas as pd
import numpy as np
import os

# -----------------------------
# 1. LOAD AND EXPLORE
# -----------------------------

# Load the cleaned CSV produced by Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print shape: (rows, columns)
print(f"Loaded data: {df.shape}")

# Print first 5 rows for a quick sanity check
print("\nFirst 5 rows:")
print(df.head())

# Overall averages across all stories
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:,.3f}")
print(f"Average comments: {avg_comments:,.3f}")

# -----------------------------
# 2. NUMPY STATISTICS
# -----------------------------

# Convert score column to a NumPy array for explicit NumPy usage
scores = df["score"].to_numpy()

mean_score   = np.mean(scores)
median_score = np.median(scores)
std_score    = np.std(scores)
max_score    = np.max(scores)
min_score    = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:,.3f}")
print(f"Median score : {median_score:,.3f}")
print(f"Std deviation: {std_score:,.3f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Category with the most stories
# value_counts() returns counts sorted descending; idxmax picks the top one
category_counts  = df["category"].value_counts()
top_category     = category_counts.idxmax()
top_category_cnt = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_category_cnt} stories)")

# Story with the most comments
# idxmax() returns the row index of the highest num_comments value
most_commented_idx   = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]

print(f'Most commented story: "{most_commented_title}"  — {most_commented_count} comments')

# -----------------------------
# 3. ADD NEW COLUMNS
# -----------------------------

# engagement: how much discussion a story generates per upvote.
# We add 1 to score to avoid division by zero for any score=0 edge cases.
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular: True if this story's score is above the overall average score.
# avg_score was computed above using pandas .mean(), consistent with the data.
df["is_popular"] = df["score"] > avg_score

# Quick check — show the two new columns alongside key fields
print("\nSample with new columns:")
print(df[["title", "score", "num_comments", "engagement", "is_popular"]].head())

# -----------------------------
# 4. SAVE THE RESULT
# -----------------------------

os.makedirs("data", exist_ok=True)

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
