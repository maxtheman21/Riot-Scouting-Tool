from PIL import Image, ImageDraw, ImageFont
import requests
import json

# TODO
# Bottom Part = Recent 10 matches in Ranked Solo andor Ranked Flex
# Split to Top / Right / Middle / Bottom? Parts


# Configuration for layout
CHAMPION_ICON_SIZE = (40, 40)  # Width, Height of champion icons
FONT_PATH = "Image/Roboto-Black.ttf"  # Path to a TTF font file (e.g., Arial.ttf or DejaVuSans.ttf)
with open('championKey/champion_name_key_map.json', 'r') as file:
    key = json.load(file)
OUTPUT_IMAGE_SIZE = (2000, 1200)  # Output image dimensions
ROW_SPACING = 40  # Space between rows within a section

# Example match data
team = [
    {"section": "Placement Matches",
        "matches": [
            {"team": "Team1", "W/L": "B", "side": "Blue",
                "picks": ["vi", "aatrox", "monkeyking", "warwick", "ashe", "jinx", "milio", "kogmaw", "masteryi", "belveth"]},
            {"team": "Team1", "W/L": "R", "side": "Red",
                "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
            {"team": "Team1", "W/L": "B", "side": "Blue",
                "picks": ["vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi"]},
            {"team": "Team1", "W/L": "R", "side": "Red",
                "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
            {"team": "Team1", "W/L": "B", "side": "Blue",
                "picks": ["vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi"]},
            {"team": "Team1", "W/L": "R", "side": "Red",
                "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
    ]},
    {"section": "Week 1",
        "matches": [
            {"team": "Team1", "W/L": "B", "side": "Blue",
                "picks": ["vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi"]},
            {"team": "Team1", "W/L": "R", "side": "Red",
                "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
            {"team": "Team1", "W/L": "B", "side": "Blue",
                "picks": ["vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi"]},
            {"team": "Team1", "W/L": "R", "side": "Red",
                "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
            {"team": "Team1", "W/L": "B", "side": "Blue",
                "picks": ["vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi", "vi"]},
            {"team": "Team1", "W/L": "R", "side": "Red",
                "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
    ]},
    # Add more sections and rows as needed...
]

# TODO
# Figure out how to display champions played in ROLE rather than pick order
# Subs?

def top_layout(team, output_file="output.jpg"):
    # Create a blank canvas
    img = Image.new("RGB", OUTPUT_IMAGE_SIZE, "beige")
    draw = ImageDraw.Draw(img)
    
    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, 20)
    small_font = ImageFont.truetype(FONT_PATH, 15)
    
    x_margin, y_margin = 50, 50  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    for section in team:
        # Draw section title
        draw.text((x_offset, y_offset), section["section"], fill="black", font=font)
        y_offset += ROW_SPACING  # Move down for the rows
        for match in section["matches"]: # BLUE
            # Draw team names and scores
            text = f"{match['team']} ({match['W/L']})"
            draw.text((x_offset, y_offset), text, fill="black", font=small_font)
            
            # Place champion icons
            icon_x = x_offset + 400  # Indent icons to the right of text
            count = 0
            for champ in match["picks"]:
                url = f"https://raw.communitydragon.org/latest/game/assets/characters/{champ}/hud/{champ}_square.png"
                champ_img = Image.open(requests.get(url, stream=True).raw).resize(CHAMPION_ICON_SIZE)
                img.paste(champ_img, (icon_x, y_offset))
                icon_x += CHAMPION_ICON_SIZE[0] + ICON_SPACING  # Space between icons
            
            y_offset += ROW_SPACING  # Move to the next row
        
        # Add spacing between sections
        y_offset += SECTION_SPACING - ROW_SPACING
        
        for match in section["matches"]: # RED
            # Draw team names and scores
            text = f"{match['team']} ({match['W/L']})"
            draw.text((x_offset, y_offset), text, fill="black", font=small_font)
            
            # Place champion icons
            icon_x = x_offset + 400  # Indent icons to the right of text
            for champ in match["picks"]:
                url = f"https://raw.communitydragon.org/latest/game/assets/characters/{champ}/hud/{champ}_square.png"
                champ_img = Image.open(requests.get(url, stream=True).raw).resize(CHAMPION_ICON_SIZE)
                img.paste(champ_img, (icon_x, y_offset))
                icon_x += CHAMPION_ICON_SIZE[0] + ICON_SPACING  # Space between icons
            
            y_offset += ROW_SPACING  # Move to the next row
        
        # Add spacing between sections
        y_offset += SECTION_SPACING - ROW_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

# TODO
# KDAs

def middle_layout(team, output_file="output.jpg"):
    ICON_SPACING = 10  # Space between icons within a row
    GAME_SPACING = 30 #Space between teams (Blue and Red)
    SECTION_SPACING = 100  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    # Create a blank canvas
    img = Image.new("RGB", OUTPUT_IMAGE_SIZE, (207, 191, 163))
    draw = ImageDraw.Draw(img)
    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, 20)
    small_font = ImageFont.truetype(FONT_PATH, 15)
    
    x_margin, y_margin = 50, 50  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    for section in team:
        # Draw section title
        draw.text((x_offset, y_offset), section["section"], fill="black", font=font)
        y_offset += ROW_SPACING  # Move down for the rows
        for match in section["matches"]: # BLUE
            if match['side'] == 'Blue':
                # Draw team names and scores
                text = f"{match['W/L']} {match['team']}"
                draw.text((x_offset, y_offset), text, fill="black", font=small_font)
                # Place champion icons
                icon_x = x_offset + 400  # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = key[champ]
                    print(ID)
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize(CHAMPION_ICON_SIZE)
                    champ_img = champ_img.convert("RGBA")
                    if count == 1 or count == 2 or count == 3 or count == 7 or count == 8:
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    img.paste(champ_img, (icon_x, y_offset), champ_img)
                    if count == 3 or count == 4 or count == 6 or count == 8: 
                        icon_x += CHAMPION_ICON_SIZE[0] + ICON_SPACING + 40  # Space between icons
                    else:
                        icon_x += CHAMPION_ICON_SIZE[0] + ICON_SPACING
                    count += 1
                y_offset += GAME_SPACING  # Move to the next row
            if match['side'] == 'Red':
                # Draw team names and scores
                text = f"{match['W/L']} ({match['team']})"
                draw.text((x_offset, y_offset), text, fill="black", font=small_font)
                
                # Place champion icons
                icon_x = x_offset + 420  # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = key[champ]
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize(CHAMPION_ICON_SIZE)
                    champ_img = champ_img.convert("RGBA")
                    if count == 1 or count == 2 or count == 3 or count == 7 or count == 8:
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    img.paste(champ_img, (icon_x, y_offset), champ_img)
                    if count == 3 or count == 5 or count == 6 or count == 9: 
                        icon_x += CHAMPION_ICON_SIZE[0] + ICON_SPACING + 40  # Space between icons
                    else:
                        icon_x += CHAMPION_ICON_SIZE[0] + ICON_SPACING
                    count += 1
                
                y_offset += GAME_SPACING  # Move to the next row
            
                # Add spacing between sections
                y_offset += SECTION_SPACING - ROW_SPACING
        y_offset += SECTION_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

# TODO
# Get week # or PC, S(emi), Q(uarter) displayed centered to the games (# of games / 2)
# Green / Red color for win/lose 

def right_layout(team, output_file="mid.jpg"):
    ICON_SPACING = 10  # Space between icons within a row
    GAME_SPACING = int(CHAMPION_ICON_SIZE[1] + (CHAMPION_ICON_SIZE[1] / 4)) #Space between teams (Blue and Red)
    SECTION_SPACING = int((CHAMPION_ICON_SIZE[1] / 2))  # Space between sections (e.g., Placement Matches, Week 1, etc.)
    # Create a blank canvas
    img = Image.new("RGB", OUTPUT_IMAGE_SIZE, (207, 191, 163))
    draw = ImageDraw.Draw(img)
    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, 20)
    
    x_margin, y_margin = 50, 50  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    for section in team:
        # Draw section title
        draw.text((x_offset, y_offset), section["section"], fill="black", font=font)
        for match in section["matches"]: # BLUE
            if match['side'] == 'Blue' and match['team'] == 'Team1':
                # Place champion icons
                icon_y = x_offset # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = key[champ]
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize(CHAMPION_ICON_SIZE)
                    champ_img = champ_img.convert("RGBA")
                    if count > 5:
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    img.paste(champ_img, (icon_y, y_offset), champ_img)
                    if count == 3:
                        icon_y += int(CHAMPION_ICON_SIZE[1] / 2)
                    if count == 1 or count == 3 or count == 5 or count == 8: # first pick, 2 picks, then 2 picks. 3 bans, then 2 bans 
                        icon_y += CHAMPION_ICON_SIZE[1] + ICON_SPACING + CHAMPION_ICON_SIZE[1]  # Empty Portrait Space to Indicate a stop in picking (i.e) BLUE SIDE: 1st pick SPACE 2nd pick 
                    else:
                        icon_y += CHAMPION_ICON_SIZE[1] + ICON_SPACING
                    count += 1
                y_offset += GAME_SPACING  # Move to the next row
            if match['side'] == 'Red' and match['team'] == 'Team1':
                # Place champion icons
                icon_y = x_offset  # Indent icons to the right of text
                count = 1
                for champ in match["picks"]:
                    ID = key[champ]
                    url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{ID}.png"
                    champ_img = Image.open(requests.get(url, stream=True).raw).resize(CHAMPION_ICON_SIZE)
                    champ_img = champ_img.convert("RGBA")
                    if count > 5:
                        data = champ_img.getdata()
                        new_data = []
                        for item in data:
                            new_alpha = int(item[3] * 0.25)  
                            new_data.append((item[0], item[1], item[2], new_alpha)) 
                        champ_img.putdata(new_data)
                    img.paste(champ_img, (icon_y, y_offset), champ_img)
                    if count == 3:
                        icon_y += int(CHAMPION_ICON_SIZE[1] / 2)
                    if count == 2 or count == 4 or count == 5 or count == 8: # 2 picks, 2 picks, then last pick. 3 bans, then 2 bans
                        icon_y += CHAMPION_ICON_SIZE[1] + ICON_SPACING + CHAMPION_ICON_SIZE[1]  # Empty Portrait Space to Indicate a stop in picking (i.e) BLUE SIDE: 1st pick SPACE 2nd pick
                    else:
                        icon_y += CHAMPION_ICON_SIZE[1] + ICON_SPACING
                    count += 1
                
                y_offset += GAME_SPACING  # Move to the next row
            
                # Add spacing between sections
        y_offset += SECTION_SPACING


    # Save the result
    img.save(output_file)
    print(f"Layout saved as {output_file}")

# TODO
# Use old code to get past 10 matches in ranked OR top 5 mastery

def bottom_layout(team, output_file="mid.jpg"):
    #Complex
    return 0

def main():
    # top_layout(team, output_file = "top.jpg")
    # middle_layout(team, output_file="mid.jpg")
    right_layout(team, output_file="right.jpg")
    # bottom_layout(team, output_file="mid.jpg")


main()
