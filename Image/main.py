from PIL import Image, ImageDraw, ImageFont
import requests
import json
from creds import *



# Configuration for layout
cred = cred()
with open('championKey/champion_name_key_map.json', 'r') as file: #JSON to convert name to ID for URL lookup
    key = json.load(file)
with open('Image\data.json', 'r') as file:
    team = json.load(file)

roles = ["Top", "Jungle", "Mid", "Bot", "Support"]
players = ["dawnbreak#free", "greattohave#NA1", "eletro#6841", "maxtheman21#coe", "armedchief#2001"] # Starting roster we are analyzing (Sample)
FONT_PATH = "Image/Roboto-Black.ttf"  # Path to a TTF font file 
College = "Coe"
CHAMPION_ICON_SIZE = 500 # Width, Height of champion icons




# GLOBAL TODO
# Resize everything so it matches the original size of the icons
# Font Color, Then Ready

def top_layout(team, output_file="positions.jpg"):
    longest = ""
    GAME_SPACING = int(CHAMPION_ICON_SIZE * 0.15) #Space between teams (Blue and Red)
    SECTION_SPACING = int(CHAMPION_ICON_SIZE * 0.5)  # Space between sections (e.g., Placement Matches, Week 1, etc.)

    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, CHAMPION_ICON_SIZE)
    count = 0
    x_margin, y_margin = CHAMPION_ICON_SIZE * 0.25, CHAMPION_ICON_SIZE * 1.25  # Starting positions
    x_offset, y_offset = x_margin, y_margin
    for player in players:
        if len(player) > len(longest): 
            longest = player.upper() # Grabs the longest username
    for char in longest:
        x_offset += font.getbbox(char)[2] # Offsets everything by that username
    icon_x = int(x_offset + CHAMPION_ICON_SIZE * 1.01)  # Indent icons to the right of text

    # Create a blank canvas
    img = Image.new("RGB", (int(x_offset * 2 + (30 * (CHAMPION_ICON_SIZE * 1.25) + GAME_SPACING) + 10 * SECTION_SPACING), int(y_offset * 1.2 + 5 * (CHAMPION_ICON_SIZE * 1.25))), "beige")
    draw = ImageDraw.Draw(img)
    
    for player in players:
        temp = player.split("#")
        import requests
        account_info = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{temp[0]}/{temp[1]}?api_key={cred}")
        puuid = account_info.json()['puuid']
        summoner_info = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={cred}")
        summoner_id = summoner_info.json()['id']
        rank_info = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={cred}")
        rank = rank_info.json()
        for queue in rank:
            if queue["queueType"] == "RANKED_SOLO_5x5": # Find Solo Queue
                rank = queue["tier"].lower()[0].upper() + queue["tier"].lower()[1:] # Finds ranked
        pos = y_offset * 1.1 + (count * CHAMPION_ICON_SIZE * 1.25) # Offsets for positions
        player = player.upper() # Upper
        x = x_offset
        for char in player[::-1]:
            char_width = font.getbbox(char)[2]  # Get the width of the character
            x -= char_width  # Move left for the next character
            draw.text((x, pos - CHAMPION_ICON_SIZE * 0.1), char, font=font, fill="black")
        if not rank: # If unranked
            rank = "Iron"
        icon_path = f"positions/Position_{rank}-{roles[count]}.png"
        icon = Image.open(icon_path).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
        img.paste(icon, ((icon_x - CHAMPION_ICON_SIZE - GAME_SPACING), int(y_offset + count * (CHAMPION_ICON_SIZE * 1.25))), mask= icon) # Pastes Role Icon
        count += 1
    for section in team["Coe"]:
        if "Week" in section["section"]:
            temp = section["section"].split(" ")
            draw.text((icon_x + int(((len(section["matches"]) * (int(CHAMPION_ICON_SIZE + (CHAMPION_ICON_SIZE / 4)))) / 2) - CHAMPION_ICON_SIZE * 0.75) * 2,   CHAMPION_ICON_SIZE * 0.375 + ( 7 * CHAMPION_ICON_SIZE)), (temp[1]).upper(), fill="black", font=font)
        else:
            draw.text((icon_x + int(((len(section["matches"]) * (int(CHAMPION_ICON_SIZE + (CHAMPION_ICON_SIZE / 4)))) / 2) - CHAMPION_ICON_SIZE * 0.75) * 2, CHAMPION_ICON_SIZE * 0.375 + (7 * CHAMPION_ICON_SIZE)), (section["section"][0]).upper(), fill="black", font=font)
        for match in section["matches"]:
            if match['W/L'] == 'W' and match['team'] == College:
                WL = "green"
            elif match['W/L'] == 'L' and match['team'] == College:
                WL = "red"
            draw.rectangle([(icon_x - 2, y_offset + int(CHAMPION_ICON_SIZE * 6)), icon_x + 1 + CHAMPION_ICON_SIZE, y_offset + int(CHAMPION_ICON_SIZE * 6) + CHAMPION_ICON_SIZE * 0.1], fill= WL)
            count = 1
            # Place champion icons
            for champ in match["picks"]:
                if count <= 5:
                    champion = champ.split(" ")
                    ID = key[champion[0]]          
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                    if champion[1] == "T":
                        pos = y_offset + 0 * (CHAMPION_ICON_SIZE * 1.25)
                    elif champion[1] == "J":
                        pos = y_offset + 1 * (CHAMPION_ICON_SIZE * 1.25)
                    elif champion[1] == "M":
                        pos = y_offset + 2 * (CHAMPION_ICON_SIZE * 1.25)
                    elif champion[1] == "A":
                        pos = y_offset + 3 * (CHAMPION_ICON_SIZE * 1.25)
                    elif champion[1] == "S":
                        pos = y_offset + 4 * (CHAMPION_ICON_SIZE * 1.25)
                    draw.rectangle([(icon_x - 2, int(pos - 2)), (icon_x + CHAMPION_ICON_SIZE* 1.01, int(pos) + CHAMPION_ICON_SIZE* 1.01)], fill=WL)
                    img.paste(champ_img, (icon_x, int(pos)))
                    count += 1
                else:
                    break
            icon_x += CHAMPION_ICON_SIZE + GAME_SPACING

        
        # Add spacing between sections
        icon_x += SECTION_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

# TODO
# KDAs
# Lines

def middle_layout(team, output_file="games.jpg"):
    ROW_SPACING = CHAMPION_ICON_SIZE  # Space between rows within a section
    ICON_SPACING = int(CHAMPION_ICON_SIZE * 0.25)  # Space between icons within a row
    GAME_SPACING = int(CHAMPION_ICON_SIZE * 0.75) #Space between teams (Blue and Red)
    SECTION_SPACING = int(CHAMPION_ICON_SIZE * 2.5)  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    x_margin, y_margin = int(CHAMPION_ICON_SIZE * 1.3), int(CHAMPION_ICON_SIZE * 1.2)  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    # Create a blank canvas
    count = 0
    for section in team["Coe"]:
        for i in section["matches"]:
            count += 1
    img = Image.new("RGB", (int(21.5*CHAMPION_ICON_SIZE), int(count*2*CHAMPION_ICON_SIZE + y_offset)), (207, 191, 163))
    draw = ImageDraw.Draw(img)

    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, int(CHAMPION_ICON_SIZE * 0.5))
    small_font = ImageFont.truetype(FONT_PATH, int(CHAMPION_ICON_SIZE * 0.35))
    
    for section in team["Coe"]:
        # Draw section title
        draw.text((x_offset, y_offset), section["section"], fill="black", font=font)
        y_offset += ROW_SPACING  # Move down for the rows
        for match in section["matches"]: # BLUE
            if match['side'] == 'Blue':
                # Draw team names and scores
                text = f"{match['W/L']} {match['team']}"
                draw.text((x_offset, y_offset), text, fill="black", font=small_font)
                # Place champion icons
                icon_x = x_offset + ((CHAMPION_ICON_SIZE + ICON_SPACING) * 6)  # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = champ.split(" ")
                    ID = ID[0]        
                    ID = key[ID]            
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE)) 
                    champ_img = champ_img.convert("RGBA")
                    if count == 4: # Pick 4 & 5 
                        icon_x += 4 * (CHAMPION_ICON_SIZE + ICON_SPACING)
                        pos = icon_x
                    elif count == 6 or count == 7 or count == 8: # Ban 1 & 2 & 3
                        pos = x_offset + ((count - 4) * (CHAMPION_ICON_SIZE + ICON_SPACING))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    elif count == 9 or count == 10: # Ban 4 & 5
                        pos = x_offset + ((count + 2) * (CHAMPION_ICON_SIZE + ICON_SPACING))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    else: # Pick 1 & 2 & 3
                        pos = icon_x
                    img.paste(champ_img, (int(pos), y_offset), champ_img)
                    if count == 1: 
                        icon_x += CHAMPION_ICON_SIZE * 2 + ICON_SPACING  # Space between icons
                    else:
                        icon_x += CHAMPION_ICON_SIZE + ICON_SPACING
                    count += 1
                y_offset += GAME_SPACING  # Move to the next row
            if match['side'] == 'Red':
                # Draw team names and scores
                text = f"{match['W/L']} ({match['team']})"
                draw.text((x_offset, y_offset), text, fill="black", font=small_font)
                
                # Place champion icons
                icon_x = x_offset + CHAMPION_ICON_SIZE / 2 + ((CHAMPION_ICON_SIZE + ICON_SPACING) * 6)  # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = champ.split(" ")
                    ID = ID[0]
                    ID = key[ID]
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                    champ_img = champ_img.convert("RGBA")
                    if count == 4: # Pick 4 & 5 
                        icon_x += CHAMPION_ICON_SIZE / 4 + 3 * (CHAMPION_ICON_SIZE + ICON_SPACING)
                        pos = icon_x
                    elif count == 6 or count == 7 or count == 8: # Ban 1 & 2 & 3
                        pos = x_offset + CHAMPION_ICON_SIZE / 2 + ((count - 4) * ((CHAMPION_ICON_SIZE + ICON_SPACING)))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    elif count == 9 or count == 10: # Ban 4 & 5
                        pos = x_offset - CHAMPION_ICON_SIZE / 2 + ((count + 2) * ((CHAMPION_ICON_SIZE + ICON_SPACING)))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    else: # Pick 1 & 2 & 3
                        pos = icon_x
                    img.paste(champ_img, (int(pos), y_offset), champ_img)
                    if count == 2 or count == 4: 
                        icon_x += CHAMPION_ICON_SIZE + ICON_SPACING + CHAMPION_ICON_SIZE  # Space between icons
                    else:
                        icon_x += CHAMPION_ICON_SIZE + ICON_SPACING
                    count += 1
                y_offset += GAME_SPACING  # Move to the next row
            
                # Add spacing between sections
                y_offset += SECTION_SPACING - ROW_SPACING
        y_offset += SECTION_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

def right_layout(team, output_file="simplify.jpg"):
    ICON_SPACING = int(CHAMPION_ICON_SIZE * 0.15)  # Space between icons within a row
    GAME_SPACING = int(CHAMPION_ICON_SIZE + (CHAMPION_ICON_SIZE / 4)) #Space between teams (Blue and Red)
    SECTION_SPACING = int((CHAMPION_ICON_SIZE / 2))  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    font = ImageFont.truetype(FONT_PATH, CHAMPION_ICON_SIZE * 0.5)
    games = 0
    matches = 0

    # Create a blank canvas
    for section in team["Coe"]:
        matches += 1
        for i in section["matches"]:
            if i['team'] == "Coe":
                games += 1
    img = Image.new("RGB", (16 * CHAMPION_ICON_SIZE, int( CHAMPION_ICON_SIZE * matches + 1.15 * games * CHAMPION_ICON_SIZE)), (207, 191, 163))
    draw = ImageDraw.Draw(img)
    
    x_margin, y_margin = int(CHAMPION_ICON_SIZE * 0.5), int(CHAMPION_ICON_SIZE * 0.5)  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    for section in team["Coe"]:
        # Draw section title
        pos = y_offset + int(((len(section["matches"]) * GAME_SPACING) / 2) - CHAMPION_ICON_SIZE * 0.35)
        if "Week" in section["section"]:
            temp = section["section"].split(" ")
            draw.text((x_offset / 6, pos), (temp[1]).upper(), fill="black", font=font)
        else:
            draw.text((x_offset / 6, pos), (section["section"][0]).upper(), fill="black", font=font)
        for match in section["matches"]: 
            if match['W/L'] == 'W' and match['team'] == College:
                draw.rectangle([(x_offset - CHAMPION_ICON_SIZE * 0.1, y_offset), (x_offset, y_offset + CHAMPION_ICON_SIZE)], fill="green")
            if match['W/L'] == 'L' and match['team'] == College:
                draw.rectangle([(x_offset - CHAMPION_ICON_SIZE * 0.1, y_offset), (x_offset, y_offset + CHAMPION_ICON_SIZE)], fill="red")
            if match['side'] == 'Blue' and match['team'] == College: # BLUE
                # Place champion icons
                icon_y = x_offset # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = champ.split(" ")
                    ID = ID[0]
                    ID = key[ID]
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                    champ_img = champ_img.convert("RGBA")
                    if count > 5:
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    img.paste(champ_img, (icon_y, y_offset), champ_img)
                    if count == 5:
                        icon_y += int(CHAMPION_ICON_SIZE / 1.5)
                    if count == 3 or count == 8:
                        icon_y += int(CHAMPION_ICON_SIZE / 2)
                    if count == 1 or count == 3: # first pick, 2 picks, then 2 picks. 3 bans, then 2 bans 
                        icon_y += (CHAMPION_ICON_SIZE + ICON_SPACING) * 2  # Empty Portrait Space to Indicate a stop in picking (i.e) BLUE SIDE: 1st pick SPACE 2nd pick 
                    else:
                        icon_y += CHAMPION_ICON_SIZE + ICON_SPACING
                    count += 1
                y_offset += GAME_SPACING  # Move to the next row
            if match['side'] == 'Red' and match['team'] == College: # RED
                # Place champion icons
                icon_y = x_offset  # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = champ.split(" ")
                    ID = ID[0]       
                    ID = key[ID]             
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                    champ_img = champ_img.convert("RGBA")
                    if count > 5:
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    img.paste(champ_img, (icon_y, y_offset), champ_img)
                    if count == 5:
                        icon_y += int(CHAMPION_ICON_SIZE / 1.5)
                    if count == 3 or count == 8:
                        icon_y += int(CHAMPION_ICON_SIZE / 2)
                    if count == 2 or count == 4: # 2 picks, 2 picks, then last pick. 3 bans, then 2 bans
                        icon_y += (CHAMPION_ICON_SIZE + ICON_SPACING) * 2  # Empty Portrait Space to Indicate a stop in picking (i.e) BLUE SIDE: 1st pick SPACE 2nd pick
                    else:
                        icon_y += CHAMPION_ICON_SIZE + ICON_SPACING
                    count += 1
                
                y_offset += GAME_SPACING  # Move to the next row
            
                # Add spacing between sections
        y_offset += SECTION_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

# TODO
# Use old code to get past 10 matches in ranked OR top 5 mastery
# Remove any static numbers

def bottom_layout(team, output_file="scout.jpg"):
    #Complex
    return 0

def master_image(college):
    return 0

# Work on combining all these images together w/ team name as outputfile
def main():
    top_layout(team, output_file = "top.jpg")
    # middle_layout(team, output_file="mid.jpg")
    # right_layout(team, output_file="right.jpg")
    # bottom_layout(team, output_file="mid.jpg")
    # master_image(team name)


main()
