import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load your CSV
df = pd.read_csv("title_search_sn_clean.csv", sep=';')

# Parse date and extract year
df["coverDate"] = pd.to_datetime(df["coverDate"])
df["year"] = df["coverDate"].dt.year

# Count articles per year
articles_per_year = df["year"].value_counts().sort_index()

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    articles_per_year.index,
    articles_per_year.values,
    color="#2563eb",
    edgecolor="white",
    linewidth=0.5,
    width=0.7
)

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.3,
        str(int(height)),
        ha="center", va="bottom",
        fontsize=9, color="#333333"
    )

ax.set_title("Number of Articles per Year", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Articles", fontsize=12)
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.set_xticks(articles_per_year.index)
ax.tick_params(axis="x", rotation=45)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("articles_per_year_sna.png", dpi=150)
plt.show()