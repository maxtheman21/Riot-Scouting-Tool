from PIL import Image, ImageDraw, ImageFont
import requests
import json
from creds import *
from data import *



# Configuration for layout
image_path = "Image/"
team = teams()
cred = cred()

with open('championKey/champion_name_key_map.json', 'r') as file: #JSON to convert name to ID for URL lookup
    key = json.load(file)


roles = ["Top", "Jungle", "Mid", "Bot", "Support"]
players = players()
FONT_PATH = "Roboto-Black.ttf"  # Path to a TTF font file 
college = college()
CHAMPION_ICON_SIZE = 100 # Width, Height of champion icons

# GLOBAL TODO
# Font Color, Then Ready

def top_layout(team, output_file="positions.png"):
    longest = 0
    count = 0
    scount = 0
    gcount = 0
    GAME_SPACING = int(CHAMPION_ICON_SIZE * 0.15) #Space between teams (Blue and Red)
    SECTION_SPACING = int(CHAMPION_ICON_SIZE * 0.5)  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    font = ImageFont.truetype(FONT_PATH, int(CHAMPION_ICON_SIZE * 0.5))
    x_margin, y_margin = CHAMPION_ICON_SIZE * 0.25, CHAMPION_ICON_SIZE * 1.25  # Starting positions
    x_offset, y_offset = x_margin, y_margin


    for player in players:
        length = 0
        player = player.upper()
        for char in player:
            length += font.getbbox(char)[2]
        if length > longest:
            longest = length
    x_offset += longest + CHAMPION_ICON_SIZE * 0.1 # Offsets everything by that username

    icon_x = int(x_offset + CHAMPION_ICON_SIZE * 1.01)  # Indent icons to the right of text
    for section in team[college]:
        scount += 1
        for i in section["matches"]:
            gcount += 1

    # Create a blank canvas
    img = Image.new("RGBA", (int(x_offset + ((1 + gcount) * (CHAMPION_ICON_SIZE + GAME_SPACING) + scount * SECTION_SPACING)), int(y_offset * 1.8 + 5 * (CHAMPION_ICON_SIZE * 1.25))), (0, 0, 0, 0,))
    draw = ImageDraw.Draw(img)
    
    for player in players:
        temp = player.split("#")
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
        x = x_offset - CHAMPION_ICON_SIZE * 0.1
        for char in player[::-1]:
            char_width = font.getbbox(char)[2]  # Get the width of the character
            x -= char_width  # Move left for the next character
            draw.text((x, pos), char, font=font, fill="black")
        if not rank: # If unranked
            rank = "Iron"
        icon_path = f"positions/Position_{rank}-{roles[count]}.png"
        icon = Image.open(icon_path).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
        img.paste(icon, ((icon_x - CHAMPION_ICON_SIZE - GAME_SPACING), int(y_offset + count * (CHAMPION_ICON_SIZE * 1.25))), mask= icon) # Pastes Role Icon
        count += 1
    for section in team[college]:
        scout = 0
        for i in section["matches"]: 
            for j in section["matches"][i]:
                match = section["matches"][i][j]
                if match["team"] == college:
                    scout += 1
                    if match['W/L'] == 'W':
                        WL = "green"
                    elif match['W/L'] == 'L':
                        WL = "red"
                    draw.rectangle([(icon_x - CHAMPION_ICON_SIZE * 0.03, y_offset + int(CHAMPION_ICON_SIZE * 6)), icon_x + CHAMPION_ICON_SIZE * 1.03, y_offset + int(CHAMPION_ICON_SIZE * 6) + CHAMPION_ICON_SIZE * 0.1], fill= WL)
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
                            draw.rectangle([(icon_x - CHAMPION_ICON_SIZE * 0.03, int(pos - CHAMPION_ICON_SIZE * 0.03)), (icon_x + CHAMPION_ICON_SIZE * 1.03, int(pos) + CHAMPION_ICON_SIZE* 1.03)], fill=WL)
                            img.paste(champ_img, (icon_x, int(pos)))
                            count += 1
                        else:
                            break
                    icon_x += CHAMPION_ICON_SIZE + GAME_SPACING        
        if "Week" in section["section"]:
            temp = section["section"].split(" ")
            draw.text((icon_x - int(CHAMPION_ICON_SIZE * scout / 1.5),   CHAMPION_ICON_SIZE * 0.375 + ( 7 * CHAMPION_ICON_SIZE)), (temp[1]).upper(), fill="black", font=font)
        else:
            draw.text((icon_x - int(CHAMPION_ICON_SIZE * scout / 1.5), CHAMPION_ICON_SIZE * 0.375 + (7 * CHAMPION_ICON_SIZE)), (section["section"][0]).upper(), fill="black", font=font)
        # Add spacing between sections
        icon_x += SECTION_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

# TODO
# Lines
# Change W/L Font

def middle_layout(team, output_file="games.png"):
    ROW_SPACING = CHAMPION_ICON_SIZE  # Space between rows within a section
    ICON_SPACING = int(CHAMPION_ICON_SIZE * 0.25)  # Space between icons within a row
    GAME_SPACING = int(CHAMPION_ICON_SIZE * 0.75) #Space between teams (Blue and Red)
    SECTION_SPACING = int(CHAMPION_ICON_SIZE * 2.5)  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    x_margin, y_margin = int(CHAMPION_ICON_SIZE * 1.3), int(CHAMPION_ICON_SIZE * 1.2)  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    current = []
    previous = []
    count = 0
    sec = 0
    for section in team[college]:
        sec += 1
        for i in section["matches"]:
            print(i)
            count += 1
    sec = round(sec/2)
    # Create a blank canvas
    img = Image.new("RGBA", (int(21.5*CHAMPION_ICON_SIZE*2), int(((count)+sec)*1.5*CHAMPION_ICON_SIZE + y_offset)), (0, 0, 0 ,0)) #1st error will appear here, count+sec isn't correct
    draw = ImageDraw.Draw(img)

    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, int(CHAMPION_ICON_SIZE * 0.5))
    small_font = ImageFont.truetype(FONT_PATH, int(CHAMPION_ICON_SIZE * 0.35))
    draw.line(((21.25*CHAMPION_ICON_SIZE + CHAMPION_ICON_SIZE / 3, y_offset), (21.25*CHAMPION_ICON_SIZE + CHAMPION_ICON_SIZE / 3, (count+sec)*CHAMPION_ICON_SIZE)), fill = "gray", width = int(CHAMPION_ICON_SIZE/50))
    for section in team[college]:
        if sec == 0:
            x_offset = 21.5*CHAMPION_ICON_SIZE + CHAMPION_ICON_SIZE / 2
            y_offset = y_margin
        # Draw section title
        draw.text((x_offset, y_offset), section["section"], fill="black", font=font)
        y_offset += ROW_SPACING  # Move down for the rows
        for i in section["matches"]: 
            for j in section["matches"][i]:
                match = section["matches"][i][j]
                if j == 'Blue':
                    count = 1
                    icon_x = x_offset + ((CHAMPION_ICON_SIZE + ICON_SPACING) * 6)  # Indent icons to the right of text
                    next_row = GAME_SPACING
                elif j == 'Red':
                    count = 11
                    icon_x = x_offset + CHAMPION_ICON_SIZE / 2 + ((CHAMPION_ICON_SIZE + ICON_SPACING) * 6)  # Indent icons to the right of text
                    next_row = GAME_SPACING + SECTION_SPACING - ROW_SPACING
                else:
                    print("Error")
                # Draw team names and scores
                text = f"{match['W/L']} {match['team']}"
                draw.text((x_offset, y_offset), text, fill="black", font=small_font)
                # Place champion icons
                for champ in match["picks"]:
                    ID = champ.split(" ")
                    ID = ID[0]
                    if ID == "":
                        ID = -1
                    else:        
                        ID = key[ID]           
                    if ID in previous and match["team"] == college:
                        print(champ)
                    if match["team"] == college:
                       current.append(ID) 
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
                            new_alpha = int(item[3] * 0.75)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    elif count == 9 or count == 10: # Ban 4 & 5
                        pos = x_offset + ((count + 2) * (CHAMPION_ICON_SIZE + ICON_SPACING))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.75)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    elif count < 11: # Pick 1 & 2 & 3
                        pos = icon_x
                    if count == 1: 
                        icon_x += CHAMPION_ICON_SIZE * 2 + ICON_SPACING  # Space between icons
                    elif count < 11:
                        icon_x += CHAMPION_ICON_SIZE + ICON_SPACING
                        
                    # RED SIDE
                    if count == 14: # Pick 4 & 5 
                        icon_x += CHAMPION_ICON_SIZE / 4 + 3 * (CHAMPION_ICON_SIZE + ICON_SPACING)
                        pos = icon_x
                    elif count == 16 or count == 17 or count == 18: # Ban 1 & 2 & 3
                        pos = x_offset + CHAMPION_ICON_SIZE / 2 + ((count - 14) * ((CHAMPION_ICON_SIZE + ICON_SPACING)))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.75)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    elif count == 19 or count == 20: # Ban 4 & 5
                        pos = x_offset - CHAMPION_ICON_SIZE / 2 + ((count + 2 - 10) * ((CHAMPION_ICON_SIZE + ICON_SPACING)))  # Indent icons to the right of text    
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.75)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    elif count > 10: # Pick 1 & 2 & 3
                        pos = icon_x
                    img.paste(champ_img, (int(pos), y_offset), champ_img)
                    if count == 12 or count == 14: 
                        icon_x += CHAMPION_ICON_SIZE + ICON_SPACING + CHAMPION_ICON_SIZE  # Space between icons
                    elif count > 10:
                        icon_x += CHAMPION_ICON_SIZE + ICON_SPACING
                    count += 1
                y_offset += next_row # Move to the next row
                if match["team"] == college:
                    previous = current
        sec -= 1
        draw.line(((x_offset + CHAMPION_ICON_SIZE, y_offset - GAME_SPACING), (x_offset + 15 * (ICON_SPACING + CHAMPION_ICON_SIZE), y_offset - GAME_SPACING)), fill = "gray", width = int(CHAMPION_ICON_SIZE / 50))
        previous = []


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

def right_layout(team, output_file="simplify.png"):
    ICON_SPACING = int(CHAMPION_ICON_SIZE * 0.15)  # Space between icons within a row
    GAME_SPACING = int(CHAMPION_ICON_SIZE + (CHAMPION_ICON_SIZE / 4)) #Space between teams (Blue and Red)
    SECTION_SPACING = int((CHAMPION_ICON_SIZE / 2))  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    font = ImageFont.truetype(FONT_PATH, CHAMPION_ICON_SIZE * 0.75)
    games = 0
    matches = 0
    # Create a blank canvas
    for section in team[college]:
        cnt = 0
        matches += 1
        for i in section["matches"]:
            for j in section["matches"][i]:
                if section["matches"][i][j]["team"] == college:
                    games += 1
                    
    img = Image.new("RGBA", (16 * CHAMPION_ICON_SIZE + int(CHAMPION_ICON_SIZE * 0.5), int(matches * games * CHAMPION_ICON_SIZE)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    x_margin, y_margin = int(CHAMPION_ICON_SIZE * 0.5), int(CHAMPION_ICON_SIZE * 0.5)  # Starting positions
    x_offset = int(x_margin + CHAMPION_ICON_SIZE * 0.25)
    y_offset = y_margin
    
    for section in team[college]:
        scout = 0
        for i in section["matches"]:
            for j in section["matches"][i]:
                if section["matches"][i][j]["team"] == college:
                    scout += 1
        # Draw section title
        pos = y_offset + int(((scout * GAME_SPACING) / 2) - CHAMPION_ICON_SIZE * 0.35)
        if "Week" in section["section"]:
            temp = section["section"].split(" ")
            draw.text((x_offset / 2 - CHAMPION_ICON_SIZE * 0.25, pos - CHAMPION_ICON_SIZE * 0.25), (temp[1]).upper(), fill="black", font=font)
        else:
            draw.text((x_offset / 2 - CHAMPION_ICON_SIZE * 0.25, pos - CHAMPION_ICON_SIZE * 0.25), (section["section"][0]).upper(), fill="black", font=font)
        for i in section["matches"]:
            for j in section["matches"][i]: 
                match = section["matches"][i][j]
                if match['W/L'] == 'W' and match['team'] == college:
                    draw.rectangle([(x_offset - CHAMPION_ICON_SIZE * 0.1, y_offset), (x_offset, y_offset + CHAMPION_ICON_SIZE)], fill="green")
                if match['W/L'] == 'L' and match['team'] == college:
                    draw.rectangle([(x_offset - CHAMPION_ICON_SIZE * 0.1, y_offset), (x_offset, y_offset + CHAMPION_ICON_SIZE)], fill="red")
                if j == 'Blue':
                    if match['team'] == college: # BLUE
                        # Place champion icons
                        icon_y = x_offset # Indent icons to the right of text
                        count = 1
                        for champ in match["picks"]:
                            if count < 6:
                                ID = champ.split(" ")
                                ID = ID[0]
                                if ID == '':
                                    ID = -1
                                else:
                                    ID = key[ID] 
                                url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                                champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                                champ_img = champ_img.convert("RGBA")
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
                    else:
                        count = 1
                        icon_y = int(CHAMPION_ICON_SIZE * 8.9) + x_offset
                        for champ in match["picks"]:
                            if count > 5:
                                ID = champ.split(" ")
                                ID = ID[0]
                                if ID == '':
                                    ID = -1
                                else:
                                    ID = key[ID] 
                                url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                                champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                                champ_img = champ_img.convert("RGBA")
                                data = champ_img.getdata()
                                new_data = []
                                for item in data:
                                    new_alpha = int(item[3] * 0.75)  
                                    new_data.append((item[0], item[1], item[2], new_alpha)) 
                                champ_img.putdata(new_data)
                                img.paste(champ_img, (icon_y, y_offset), champ_img)
                                if count == 8:
                                    icon_y += int(CHAMPION_ICON_SIZE / 2)
                                icon_y += CHAMPION_ICON_SIZE + ICON_SPACING
                            count += 1
                if j == 'Red':
                    if match['team'] == college: # RED
                        # Place champion icons
                        icon_y = x_offset  # Indent icons to the right of text
                        count = 1
                        for champ in match["picks"]:
                            if count < 6:
                                ID = champ.split(" ")
                                ID = ID[0]       
                                if ID == '':
                                    ID = -1
                                else:
                                    ID = key[ID]             
                                url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                                champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                                champ_img = champ_img.convert("RGBA")
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
                    else:
                        count = 1
                        icon_y = int(CHAMPION_ICON_SIZE * 8.9) + x_offset
                        for champ in match["picks"]:
                            if count > 5:
                                ID = champ.split(" ")
                                ID = ID[0]
                                if ID == '':
                                    ID = -1
                                else:
                                    ID = key[ID] 
                                url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                                champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))
                                champ_img = champ_img.convert("RGBA")
                                data = champ_img.getdata()
                                new_data = []
                                for item in data:
                                    new_alpha = int(item[3] * 0.75)  
                                    new_data.append((item[0], item[1], item[2], new_alpha)) 
                                champ_img.putdata(new_data)
                                img.paste(champ_img, (icon_y, y_offset), champ_img)
                                if count == 8:
                                    icon_y += int(CHAMPION_ICON_SIZE / 2)
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

def bottom_layout(team, output_file="topchamps.png"):
    ICON_SPACING = int(CHAMPION_ICON_SIZE * 0.15)  # Space between icons within a row
    PLAYER_SPACING = int(CHAMPION_ICON_SIZE / 2) #Space between teams (Blue and Red)
    longest = 0
    x_margin, y_margin = CHAMPION_ICON_SIZE * 0.25, CHAMPION_ICON_SIZE * 0.5  # Starting positions
    x_offset, y_offset = x_margin, y_margin
    font = ImageFont.truetype(FONT_PATH, int(CHAMPION_ICON_SIZE * 0.5))
    
    for player in players:
        length = 0
        player = player.upper()
        for char in player:
            length += font.getbbox(char)[2]
        if length > longest:
            longest = length
    x_offset += longest + CHAMPION_ICON_SIZE * 0.1 # Offsets everything by that username

    icon_x = int(x_offset + CHAMPION_ICON_SIZE / 4)  # Indent icons to the right of text
    
    img = Image.new("RGBA", (int(CHAMPION_ICON_SIZE + x_offset + 5 * CHAMPION_ICON_SIZE + ICON_SPACING), CHAMPION_ICON_SIZE * 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    count = 0
    for player in players:
        pos = y_offset + (count * CHAMPION_ICON_SIZE * 1.5) + CHAMPION_ICON_SIZE / 4 # Offsets for positions
        player = player.upper() # Upper
        x = x_offset
        for char in player[::-1]:
            char_width = font.getbbox(char)[2]  # Get the width of the character
            x -= char_width  # Move left for the next character
            draw.text((x, pos), char, font=font, fill="black")
        count += 1

    for player in players:
        temp = player.split("#")
        account_info = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{temp[0]}/{temp[1]}?api_key={cred}")
        puuid = account_info.json()['puuid']
        temp = icon_x
        mastery = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=5&api_key={cred}")
        for i in mastery.json():
            ID = i["championId"]
            url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
            champ_img = Image.open(requests.get(url, stream=True).raw).resize((CHAMPION_ICON_SIZE, CHAMPION_ICON_SIZE))            
            img.paste(champ_img, (temp, int(y_offset)))
            temp += CHAMPION_ICON_SIZE + ICON_SPACING
        y_offset += CHAMPION_ICON_SIZE + PLAYER_SPACING
    
    img.save(output_file)
    print(f"Layout saved as {output_file}")

def master_image(output_file = "combined.png"):
    top = Image.open(f"{image_path}top.png")
    mid = Image.open(f"{image_path}mid.png")
    right = Image.open(f"{image_path}right.png")
    bot = Image.open(f"{image_path}bot.png")
    logo = Image.open(f"{image_path}college.png").resize((top.height,top.height))
    
    # Define height and width and make canvas
    total_width = max((mid.width + right.width), (logo.width + top.width + right.width))
    total_height = (mid.height + top.height)
    super_image = Image.new("RGB", (total_width, total_height), "beige")

    # Paste the images into the final layout
    super_image.paste(logo, (0, 0), mask= logo)
    super_image.paste(top, (logo.width, 0), mask= top)
    super_image.paste(mid, (int((total_width - mid.width - right.width)/2), top.height), mask= mid)
    super_image.paste(bot, (total_width - bot.width, total_height - bot.height), mask= bot)
    super_image.paste(right, (max(mid.width, (logo.width + top.width)), 0), mask= right) 

    # Save the final image
    super_image.save(output_file)
    print(f"Layout saved as {output_file}")

# Work on combining all these images together w/ team name as outputfile
top_layout(team, output_file = f"{image_path}top.png")
middle_layout(team, output_file=f"{image_path}mid.png")
right_layout(team, output_file=f"{image_path}right.png")
bottom_layout(team, output_file = f"{image_path}bot.png")
master_image(output_file = f"{image_path}main.png")


