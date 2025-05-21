import pandas as pd
import re

# Load the CSV
df = pd.read_csv("results_with_links.csv")

# Combine all known irrelevant entries from your list
additional_excludes = {
    "speaker", "joseph estrada", "makati", "reapportioning", "kalinga", "apayao",
    "kalina-apayao", "gloria macapagal arroyo", "supreme court", "repportioning",
    "genuine opposition", "senate", "dinagat island", "pangasinan", "eduardo joson",
    "marikina", "sultan kudarat", "taguig", "pateros", "parañaque", "eduardo zialcita",
    "winston garcia", "php", "senators", "philippines", "padrino system", "batangas",
    "laguna", "paolo duterte", "sara duterte", "martin romualdez", "bongbong marcos",
    "rodrigo duterte", "alan peter cayetano", "national unity party", "facebook", "bts",
    "congress", "puerto princesa", "maguindanao", "talitay", "party-switching", "mar roxas",
    "karlo nograles", "midas hotel and casino", "danilo suarez", "ronaldo zamora",
    "toby tiangco", "bicolanos", "mikee romero", "tito sotto", "prospero nograles",
    "gma news and public affairs", "edcel lagman", "albay", "imelda marcos", "lani mercado",
    "lucy torres", "manny pacquiao", "malolos", "noynoy aquino", "iggy arroyo", "comelec"
}

# Also exclude these common issues
exclude_exact = {
    "Independent", "Party-list system", "Other party-list representatives",
    "Party-list Coalition", "Party-list", "party-list"
}

# Keywords that often appear in irrelevant rows
exclude_keywords = [
    "/", "representative", "rep.", "cong.", "congressman", "mp", "hon.", "honorable",
    "commission", "department", "jr", "sr", "ii", "iii", "iv", "v", "vi",
    "quezon", "palawan", "davao", "manila", "cebu", "bataan", "zamboanga", "mindoro"
]

# Prepare and standardize
df["party_name_cleaned"] = df["party_name"].astype(str)

def is_invalid(name):
    name_lower = name.lower()

    # Exact exclusions
    if name in exclude_exact:
        return True

    # Additional full-name exclusions
    if name_lower.strip() in additional_excludes:
        return True

    # Keyword match
    if any(kw in name_lower for kw in exclude_keywords):
        return True

    # Fractions like "54 / 304"
    if re.match(r"^\d+\s*/\s*\d+$", name):
        return True

    # Starts with lowercase letter
    if re.match(r"^[a-z]", name):
        return True

    # Has year
    if re.search(r"\b(19|20)\d{2}\b", name):
        return True

    # "Firstname M. Lastname" pattern
    if re.match(r"^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$", name):
        return True

    # Multi-word where second or later word starts lowercase
    if re.match(r"^[A-Z][a-z]+( [a-z]+\b)+", name):
        return True

    # Ends in Jr/Sr/III etc.
    if re.search(r"\b(jr|sr|ii|iii|iv|v|vi)\.?$", name_lower):
        return True

    # Contains numbers
    if re.search(r"\d", name):
        return True

    return False

# Apply filter
df = df[~df["party_name_cleaned"].apply(is_invalid)]

# Drop helper column
df = df.drop(columns=["party_name_cleaned"])

# Final cleanup
df = df.drop_duplicates().reset_index(drop=True)
df.to_csv("results_with_links_cleaned.csv", index=False)

print("✅ Cleaned data saved to results_with_links_cleaned.csv")
