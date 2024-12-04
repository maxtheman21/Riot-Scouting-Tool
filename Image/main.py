from PIL import Image, ImageDraw, ImageFont
import requests

# TODO
# Blue Side / Red Side
# Bottom Part = Recent 10 matches in Ranked Solo andor Ranked Flex
# Split to Top / Right / Middle / Bottom? Parts
# KDAs
# WL
# Colors & Fonts


# Configuration for layout
CHAMPION_ICON_SIZE = (40, 40)  # Width, Height of champion icons
FONT_PATH = "Image/Roboto-Black.ttf"  # Path to a TTF font file (e.g., Arial.ttf or DejaVuSans.ttf)
OUTPUT_IMAGE_SIZE = (2000, 1200)  # Output image dimensions
SECTION_SPACING = 150  # Space between sections (e.g., Placement Matches, Week 1, etc.)
ROW_SPACING = 60  # Space between rows within a section
ICON_SPACING = 10  # Space between icons within a row

# Example match data
team = [
    {"section": "Placement Matches",
     "matches": [
         {"team": "Team", "W/L": "Win",
          "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
         {"team": "Team", "W/L": "Loss",
          "picks": ["ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko", "ekko"]},
     ]}
    # Add more sections and rows as needed...
]

def create_layout(matches, output_file="output.jpg"):
    # Create a blank canvas
    img = Image.new("RGB", OUTPUT_IMAGE_SIZE, "beige")
    draw = ImageDraw.Draw(img)
    
    # Load a font for text
    font = ImageFont.truetype(FONT_PATH, 20)
    small_font = ImageFont.truetype(FONT_PATH, 15)
    
    x_margin, y_margin = 50, 50  # Starting positions
    x_offset = x_margin
    y_offset = y_margin
    
    for section in matches:
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

# Example usage
create_layout(team)
