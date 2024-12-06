import json

# Load the champion data from the JSON file
with open("./championKey/champion.json", "r", encoding="utf-8") as file:
    champion_data = json.load(file)

# Create a mapping of champion names to their IDs
champion_id_name_map = {}

for champion_name, champion_info in champion_data["data"].items():
    id = champion_info["id"]
    id = id.lower()
    champion_id_name_map[(champion_info["id"]).lower()] = champion_info["key"]

# Write the champion name to ID mapping to a new JSON file
with open("./championKey/champion_name_key_map.json", "w", encoding="utf-8") as outfile:
    json.dump(champion_id_name_map, outfile, indent=4)

print("Champion name and ID mapping has been written to 'champion_name_key_map.json'")
