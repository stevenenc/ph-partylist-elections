import json

# Load the raw JSON
with open("partylist_attributes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalize keys (convert non-breaking space to regular space)
for entry in data:
    for key in list(entry.keys()):
        normalized_key = key.replace("\u00A0", " ")
        if normalized_key != key:
            entry[normalized_key] = entry.pop(key)

# Optional: Save to a new file
with open("partylist_attributes_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ JSON keys normalized and saved to partylist_attributes_cleaned.json")
