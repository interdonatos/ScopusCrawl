import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load data
df = pd.read_csv("crisis_results_new.csv", sep=';')
df["coverDate"] = pd.to_datetime(df["coverDate"])
df["year"] = df["coverDate"].dt.year

# Load social network keywords
with open("./data/sn_list.txt") as f:
    sn_list = [line.strip().lower() for line in f if line.strip()]

# For each SN, count how many titles mention it per year
def mentions(title, keyword):
    return keyword in str(title).lower()

counts = {}
for sn in sn_list:
    counts[sn] = df[df["title"].apply(lambda t: mentions(t, sn))].groupby("year").size()

sn_df = pd.DataFrame(counts).fillna(0).astype(int)
# Remove SNs that never appear
sn_df = sn_df.loc[:, sn_df.sum() > 0]
sn_df = sn_df.sort_index()

# "Other" = articles that don't match any SN in the list
matched = df[df["title"].apply(lambda t: any(mentions(t, sn) for sn in sn_list))]
unmatched = df[~df.index.isin(matched.index)]
#sn_df["other"] = unmatched.groupby("year").size().reindex(sn_df.index).fillna(0).astype(int)

# --- Plot ---
fig, ax = plt.subplots(figsize=(14, 7))

# Color palette — extend if you have many SNs
colors = [
    "#2563eb",  # facebook    - blue
    "#16a34a",  # youtube     - green
    "#dc2626",  # linkedin    - red
    "#d97706",  # reddit      - amber
    "#7c3aed",  # twitter     - purple
    "#059669",  # tiktok      - emerald
    "#db2777",  # pinterest   - pink
    "#65a30d",  # weibo       - lime
    "#c2410c",  # discord     - burnt orange
    "#0891b2",  # instagram   - cyan
    "#b45309",  # threads     - dark amber
    "#9ca3af",  # bereal      - gray
    "#15803d",  # social net  → "#134e4a"  # dark teal/forest
    "#4f46e5",  # mastodon    - indigo
    "#aaaaaa",  # other       - light gray
]


# Define colors by name, not by position
color_map = {
    "facebook":       "#2563eb",
    "youtube":        "#16a34a",
    "linkedin":       "#dc2626",
    "reddit":         "#dc2626",
    "twitter":        "#d97706",
    "instagram":      "#7c3aed",
    "pinterest":      "#db2777",
    "weibo":          "#0891b2",
    "discord":        "#db2777",
    "mastodon":       "#4f46e5",
    "tiktok":         "#059669",
    "social network": "#9ca3af",
    "bereal":         "#7f1d1d",
    "bluesky":        "#4338ca",
    "other":          "#6b7280",
}

bottoms = pd.Series(0, index=sn_df.index)
bars_handles = []

for col in sn_df.columns:
    color = color_map.get(col, "#cccccc")  # fallback if name not in map
    ax.bar(sn_df.index, sn_df[col], bottom=bottoms,
           color=color, edgecolor="white", linewidth=0.5, width=0.7, label=col)
    bottoms += sn_df[col]

"""
for i, col in enumerate(sn_df.columns):
    color = colors[i % len(colors)]
    bars = ax.bar(
        sn_df.index,
        sn_df[col],
        bottom=bottoms,
        color=color,
        edgecolor="white",
        linewidth=0.5,
        width=0.7,
        label=col
    )
    bars_handles.append(bars)
    bottoms += sn_df[col]
"""
# Total label on top of each bar
for x, total in zip(sn_df.index, bottoms):
    if total > 0:
        ax.text(x, total + 0.3, str(int(total)),
                ha="center", va="bottom", fontsize=8, color="#333333")

figure_title = " Crisis Management Articles Mentioning a Social Network in the Title by Year"
ax.set_title(figure_title, fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Articles", fontsize=12)
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.set_xticks(sn_df.index)
ax.tick_params(axis="x", rotation=45)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)

#handles = [plt.Rectangle((0,0),1,1, color=colors[i % len(colors)])            for i, col in enumerate(sn_df.columns)]
handles = [plt.Rectangle((0,0),1,1, color=color_map.get(col, "#cccccc"))          for col in sn_df.columns]
labels = list(sn_df.columns)

ax.legend(handles, labels, title="Social Network", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
#ax.legend(title="Social Network", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig("articles_per_year_by_sn.png", dpi=150)
plt.show()