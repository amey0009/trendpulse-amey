
# ============================================================
# TrendPulse - Task 4: Visualise the Data (Matplotlib)
# ============================================================
# What this script does:
#   1. Loads the cleaned CSV from Task 2
#   2. Creates basic charts to visualise trends
#   3. Saves charts as PNG files in 'charts/' folder
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# ── STEP 1: Load the cleaned CSV ─────────────────────────────
print("Loading cleaned CSV file...")

csv_files = glob.glob("data/trends_cleaned_*.csv")

if not csv_files:
    print("ERROR: No cleaned CSV found. Run Task 2 first!")
    exit()

csv_file = sorted(csv_files)[-1]
df = pd.read_csv(csv_file)

print(f"Loaded {len(df)} records from {csv_file}")

# Create folder for charts
os.makedirs("charts", exist_ok=True)


# ── CHART 1: Bar Chart (Stories per Category) ─────────────────
print("Creating Chart 1...")

category_counts = df['category'].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values)

plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()
plt.savefig("charts/chart1_stories_per_category.png")
plt.show()


# ── CHART 2: Horizontal Bar (Average Score per Category) ──────
print("Creating Chart 2...")

avg_scores = df.groupby('category')['score'].mean()

plt.figure(figsize=(8, 5))
plt.barh(avg_scores.index, avg_scores.values)

plt.title("Average Score per Category")
plt.xlabel("Average Score")
plt.ylabel("Category")

plt.tight_layout()
plt.savefig("charts/chart2_avg_score_per_category.png")
plt.show()


# ── CHART 3: Pie Chart (Category Distribution) ────────────────
print("Creating Chart 3...")

plt.figure(figsize=(6, 6))
plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')

plt.title("Story Distribution by Category")

plt.tight_layout()
plt.savefig("charts/chart3_category_pie.png")
plt.show()


# ── CHART 4: Scatter Plot (Score vs Comments) ─────────────────
print("Creating Chart 4...")

plt.figure(figsize=(8, 5))
plt.scatter(df['score'], df['num_comments'])

plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.tight_layout()
plt.savefig("charts/chart4_score_vs_comments.png")
plt.show()


# ── DONE ─────────────────────────────────────────────────────
print("\nAll charts saved in 'charts/' folder:")
print(" - chart1_stories_per_category.png")
print(" - chart2_avg_score_per_category.png")
print(" - chart3_category_pie.png")
print(" - chart4_score_vs_comments.png")