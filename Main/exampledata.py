import json

def players():
    return ["player#1", "player#2", "player#3", "player#4", "player#5"] # Starting roster we are analyzing (Sample)

def college():
    return "College Name" # Needs to match the college name in the json

def teams():
    with open(r'Data\path.json', 'r') as file: # Whatever json file you are using for your team
        team = json.load(file)
    return team