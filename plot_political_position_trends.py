import pandas as pd
import json
from collections import defaultdict
import matplotlib.pyplot as plt

# Load data
template_df = pd.read_csv("partylist_template.csv")
with open("partylist_attributes_cleaned.json") as f:
    attributes_data = json.load(f)

# Step 1: Normalize political positions (remove duplicates, combine variants)
def normalize_positions(position_list):
    if not isinstance(position_list, list):
        return []

    normalized = set()
    for pos in position_list:
        if not isinstance(pos, str):
            continue
        pos_clean = pos.lower().strip()
        if pos_clean in {"1", "2", "3", "4", "]", "to"}:
            continue
        if "centre" in pos_clean or "center" in pos_clean:
            if "left" in pos_clean:
                normalized.add("centre-left")
            else:
                normalized.add("centre")
        elif "left" in pos_clean:
            normalized.add("left-wing")
        elif "right" in pos_clean:
            normalized.add("right-wing")
        elif "far-left" in pos_clean:
            normalized.add("far-left")
        else:
            normalized.add(pos_clean)

    return list(normalized)

# Clean attribute data into a mapping
party_to_position = {}
for entry in attributes_data:
    name = entry.get("party_list", "").strip()
    positions = normalize_positions(entry.get("political position", []))
    if name:
        party_to_position[name] = positions

# Step 2: Prepare merged data with year, position, and votes
template_df["party_name"] = template_df["party_name"].fillna("").str.strip()
template_df["year"] = pd.to_numeric(template_df["year"], errors="coerce")
template_df["votes"] = template_df["votes"].replace(",", "", regex=True)
template_df["votes"] = pd.to_numeric(template_df["votes"], errors="coerce")

records = []
for _, row in template_df.iterrows():
    party = row["party_name"]
    year = row["year"]
    votes = row["votes"]
    positions = party_to_position.get(party, [])
    for pos in positions:
        records.append({"year": year, "political_position": pos, "votes": votes})

# Step 3: Aggregate and plot
df = pd.DataFrame(records)
pivot_df = df.groupby(["year", "political_position"])["votes"].sum().unstack().fillna(0)

# Define custom colors
color_map = {
    "left-wing": "red",
    "centre-left": "yellow",
    "centre": "magenta",
    "right-wing": "blue"
}

# Plot with colors
ax = pivot_df.plot(
    marker='o',
    figsize=(12, 6),
    title="Trend of Political Positions in Party-list Elections Over Time",
    color=[color_map.get(col, None) for col in pivot_df.columns]
)

ax.set_xlabel("Election Year")
ax.set_ylabel("Total Votes")
ax.legend(title="Political Position")
plt.tight_layout()
plt.grid(True)
plt.show()
