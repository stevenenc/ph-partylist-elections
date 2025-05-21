import pandas as pd

# Load the cleaned fixed results
fixed_df = pd.read_csv("results_fixed_cleaned.csv")
print("Fixed CSV columns:", fixed_df.columns.tolist())

# Load the cleaned links results
links_df = pd.read_csv("results_with_links_cleaned.csv")
print("Links CSV columns:", links_df.columns.tolist())

# Rename 'Party-list' to 'party_name' to match links_df
if "Party-list" in fixed_df.columns:
    fixed_df = fixed_df.rename(columns={"Party-list": "party_name"})

# Merge the dataframes on 'party_name'
merged_df = pd.merge(
    fixed_df,
    links_df[["party_name", "party_url"]],
    on="party_name",
    how="left"
)

# Fill missing party_url with "NA"
merged_df["party_url"] = merged_df["party_url"].fillna("NA")

# Drop duplicate rows
merged_df = merged_df.drop_duplicates()

# Save to new CSV
merged_df.to_csv("merged_partylist_with_links.csv", index=False)
print("✅ Merged file saved as merged_partylist_with_links.csv (duplicates removed)")
