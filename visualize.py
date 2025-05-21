import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the cleaned CSV file
df = pd.read_csv("results_fixed_cleaned.csv")

# Ensure data types are correct
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
df['Year'] = df['Year'].astype(str)

# Create a folder to save the plots
output_folder = "plots_per_year"
os.makedirs(output_folder, exist_ok=True)

# Plot one horizontal bar chart per year
years = df['Year'].unique()

for year in sorted(years):
    yearly_data = df[df['Year'] == year].dropna(subset=['Votes'])
    yearly_data = yearly_data.sort_values('Votes')  # Smallest at top, biggest at bottom

    plt.figure(figsize=(10, max(6, len(yearly_data) * 0.4)))
    plt.barh(yearly_data['Party-list'], yearly_data['Votes'], color='skyblue')
    plt.xlabel('Votes')
    plt.title(f'Party-list Votes - {year}')
    plt.tight_layout()

    # Save the plot
    plt.savefig(f"{output_folder}/partylist_votes_{year}.png")
    plt.close()

print(f"✅ Saved one chart per year to the '{output_folder}' folder.")
