# ============================================================
# Task 4 - Visualizations (TrendPulse)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# -----------------------------
# 1. SETUP
# -----------------------------

# Load the analysed CSV produced by Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Colour palette — one distinct colour per category for Chart 2
CATEGORY_COLOURS = {
    "technology":    "#4C72B0",
    "worldnews":     "#DD8452",
    "sports":        "#55A868",
    "science":       "#C44E52",
    "entertainment": "#8172B3",
}

# ============================================================
# CHART 1 — Top 10 Stories by Score (horizontal bar chart)
# ============================================================

# Sort by score descending, take the top 10
top10 = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters so they fit on the y-axis
top10["short_title"] = top10["title"].apply(
    lambda t: t[:47] + "..." if len(t) > 50 else t
)

# Sort ascending so the highest score appears at the top of the chart
top10 = top10.sort_values("score", ascending=True)

fig1, ax1 = plt.subplots(figsize=(10, 6))

ax1.barh(top10["short_title"], top10["score"], color="#4C72B0", edgecolor="white")

ax1.set_title("Top 10 Stories by Score", fontsize=14, fontweight="bold", pad=12)
ax1.set_xlabel("Score (upvotes)", fontsize=11)
ax1.set_ylabel("Story Title", fontsize=11)

# Add score value at the end of each bar for readability
for bar, score in zip(ax1.patches, top10["score"]):
    ax1.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        str(score),
        va="center", ha="left", fontsize=9
    )

plt.tight_layout()

# savefig BEFORE show — required by spec
plt.savefig("outputs/chart1_top_stories.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig1)

print("Saved: outputs/chart1_top_stories.png")

# ============================================================
# CHART 2 — Stories per Category (bar chart, one colour per bar)
# ============================================================

# Count stories per category and sort descending
category_counts = df["category"].value_counts().sort_values(ascending=False)

# Map each category to its colour; fall back to gray for unknowns
bar_colours = [CATEGORY_COLOURS.get(cat, "#999999") for cat in category_counts.index]

fig2, ax2 = plt.subplots(figsize=(8, 5))

bars = ax2.bar(category_counts.index, category_counts.values,
               color=bar_colours, edgecolor="white")

ax2.set_title("Stories per Category", fontsize=14, fontweight="bold", pad=12)
ax2.set_xlabel("Category", fontsize=11)
ax2.set_ylabel("Number of Stories", fontsize=11)

# Add count labels on top of each bar
for bar in bars:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=10
    )

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig2)

print("Saved: outputs/chart2_categories.png")

# ============================================================
# CHART 3 — Score vs Comments (scatter plot, coloured by is_popular)
# ============================================================

# Split DataFrame into popular and non-popular groups using is_popular column
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(8, 6))

# Plot non-popular stories first (behind), then popular on top
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="#AEC6E8", alpha=0.7, edgecolors="white",
            linewidths=0.5, s=60, label="Not popular")

ax3.scatter(popular["score"], popular["num_comments"],
            color="#C44E52", alpha=0.85, edgecolors="white",
            linewidths=0.5, s=80, label="Popular (above avg score)")

ax3.set_title("Score vs Number of Comments", fontsize=14, fontweight="bold", pad=12)
ax3.set_xlabel("Score (upvotes)", fontsize=11)
ax3.set_ylabel("Number of Comments", fontsize=11)

# Legend so viewer knows what each colour means
ax3.legend(fontsize=10)

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig3)

print("Saved: outputs/chart3_scatter.png")

# ============================================================
# BONUS — Dashboard: all 3 charts in one figure
# ============================================================

fig_dash, axes = plt.subplots(1, 3, figsize=(20, 6))
fig_dash.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.01)

# --- Dashboard panel 1: Top 10 horizontal bar ---
ax_d1 = axes[0]
ax_d1.barh(top10["short_title"], top10["score"], color="#4C72B0", edgecolor="white")
ax_d1.set_title("Top 10 Stories by Score", fontsize=11, fontweight="bold")
ax_d1.set_xlabel("Score")
ax_d1.set_ylabel("Story Title")
ax_d1.tick_params(axis="y", labelsize=7)

# --- Dashboard panel 2: Stories per category ---
ax_d2 = axes[1]
ax_d2.bar(category_counts.index, category_counts.values,
          color=bar_colours, edgecolor="white")
ax_d2.set_title("Stories per Category", fontsize=11, fontweight="bold")
ax_d2.set_xlabel("Category")
ax_d2.set_ylabel("Number of Stories")
ax_d2.tick_params(axis="x", rotation=15)

# --- Dashboard panel 3: Score vs comments scatter ---
ax_d3 = axes[2]
ax_d3.scatter(not_popular["score"], not_popular["num_comments"],
              color="#AEC6E8", alpha=0.7, edgecolors="white",
              linewidths=0.5, s=40, label="Not popular")
ax_d3.scatter(popular["score"], popular["num_comments"],
              color="#C44E52", alpha=0.85, edgecolors="white",
              linewidths=0.5, s=55, label="Popular")
ax_d3.set_title("Score vs Comments", fontsize=11, fontweight="bold")
ax_d3.set_xlabel("Score")
ax_d3.set_ylabel("Comments")
ax_d3.legend(fontsize=8)

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig_dash)

print("Saved: outputs/dashboard.png")
print("\nAll charts saved to outputs/")
