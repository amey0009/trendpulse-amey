
# ============================================================
# TrendPulse - Task 3: Analyse the Data (Pandas + NumPy)
# ============================================================
# What this script does:
#   1. Loads the cleaned CSV from Task 2
#   2. Uses Pandas and NumPy to analyse the data
#   3. Finds patterns: top categories, top authors, avg scores, etc.
#   4. Saves a summary report as a CSV
# ============================================================

import pandas as pd    # For working with tabular data (like Excel in Python)
import numpy as np     # For numerical calculations
import glob
import os
from datetime import datetime

# ── STEP 1: Load the cleaned CSV from Task 2 ────────────────────────────────
print("Loading cleaned CSV file...")

csv_files = glob.glob("data/trends_cleaned_*.csv")

if not csv_files:
    print("ERROR: No cleaned CSV found in 'data/'. Run Task 2 first!")
    exit()

csv_file = sorted(csv_files)[-1]  # Pick the most recent one
print(f"Found: {csv_file}")

df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} stories.")
print(f"Columns: {list(df.columns)}\n")


# ── STEP 2: Basic overview ───────────────────────────────────────────────────
print("=" * 50)
print("BASIC OVERVIEW")
print("=" * 50)

print(f"Total stories    : {len(df)}")
print(f"Total categories : {df['category'].nunique()}")
print(f"Total authors    : {df['author'].nunique()}")
print(f"Date range       : {df['collected_at'].min()} → {df['collected_at'].max()}")


print("\nData Shape:", df.shape)   # (rows, columns)
print("Dimensions:", df.ndim)     # Should be 2 for DataFrame
print("\nSummary Statistics:")
print(df[['score', 'num_comments']].describe())  # Numeric column stats


# ── STEP 3: Stories per category ────────────────────────────────────────────
print("\n" + "=" * 50)
print("STORIES PER CATEGORY")
print("=" * 50)

category_counts = df['category'].value_counts()
for cat, count in category_counts.items():
    print(f"  {cat:<15} : {count} stories")


# ── STEP 4: Average score per category ──────────────────────────────────────
print("\n" + "=" * 50)
print("AVERAGE SCORE PER CATEGORY")
print("=" * 50)

avg_scores = df.groupby('category')['score'].mean().sort_values(ascending=False)
for cat, avg in avg_scores.items():
    print(f"  {cat:<15} : {avg:.1f} avg score")


# ── STEP 5: Top 5 stories overall (by score) ────────────────────────────────
print("\n" + "=" * 50)
print("TOP 5 STORIES (by upvote score)")
print("=" * 50)

top5 = df.nlargest(5, 'score')[['title', 'category', 'score', 'num_comments']]
for i, row in top5.iterrows():
    print(f"  Score {row['score']:>5} | [{row['category']}] {row['title'][:55]}...")


# ── STEP 6: Most active authors ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("TOP 5 MOST ACTIVE AUTHORS")
print("=" * 50)

top_authors = df['author'].value_counts().head(5)
for author, count in top_authors.items():
    print(f"  {author:<20} : {count} posts")


# ── STEP 7: NumPy stats on scores ───────────────────────────────────────────
print("\n" + "=" * 50)
print("SCORE STATISTICS (NumPy)")
print("=" * 50)

scores = np.array(df['score'])  # Convert to NumPy array for calculations

print(f"  Min score     : {np.min(scores)}")
print(f"  Max score     : {np.max(scores)}")
print(f"  Mean score    : {np.mean(scores):.1f}")
print(f"  Median score  : {np.median(scores):.1f}")
print(f"  Std deviation : {np.std(scores):.1f}")  # How spread out scores are


# ── STEP 8: Save analysis summary to CSV ────────────────────────────────────
print("\nSaving analysis summary...")

summary_rows = []

for cat in df['category'].unique():
    subset = df[df['category'] == cat]
    summary_rows.append({
        "category":       cat,
        "story_count":    len(subset),
        "avg_score":      round(subset['score'].mean(), 1),
        "max_score":      subset['score'].max(),
        "avg_comments":   round(subset['num_comments'].mean(), 1),
        "top_story":      subset.loc[subset['score'].idxmax(), 'title'][:80],
    })

summary_df = pd.DataFrame(summary_rows).sort_values("avg_score", ascending=False)

os.makedirs("data", exist_ok=True)
today = datetime.now().strftime("%Y%m%d")
summary_file = f"data/analysis_summary_{today}.csv"
summary_df.to_csv(summary_file, index=False)

print(f"Analysis summary saved to: {summary_file}")