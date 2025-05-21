import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV
df = pd.read_csv("results_fixed_cleaned.csv")

# Fix the Year column
df["Year"] = df["Year"].astype(str).str.extract(r"(\d{4})")

# Use the actual labels from the dataset
target_parties = ["Bayan Muna", "Kabataan", "Gabriela Women's Party"]

# Filter for target parties
filtered_df = df[df["Party-list"].isin(target_parties)].copy()
filtered_df["Votes"] = pd.to_numeric(filtered_df["Votes"], errors="coerce")

# Pivot the data to Year x Partylist
pivot_df = filtered_df.pivot(index="Year", columns="Party-list", values="Votes").sort_index()

# Plot
plt.figure(figsize=(10, 6))
for party in target_parties:
    if party in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[party], marker="o", label=party)

plt.title("Vote Trends Over Time: Bayan Muna, Kabataan, Gabriela")
plt.xlabel("Election Year")
plt.ylabel("Votes")
plt.legend(title="Party-list")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
