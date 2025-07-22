import cv2
import numpy as np
import os

# Load the images
large_image = cv2.imread('Data/small.png')
template_image = cv2.imread('Data/burger.png')
height, width = large_image.shape[:2]
threshold = 0.8


large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
result = cv2.matchTemplate(large_gray, template_gray, cv2.TM_CCOEFF_NORMED)

loc = np.where(result >= threshold)
start_h = loc[0][0]
start_w = loc[1][0]

cropped_image = large_image[start_h: start_h + height, start_w: start_w + width]
cropped_image = cv2.resize(cropped_image, (1344, 756))

blue = [52, 165, 277, 423, 535] # 9 x i

cropped_height = 107
cropped_width = 232

pick_w, pick_h = 535, 300 # resize the pick image to this size and then
crop_w, crop_h = 220, 105 # crop the *center* to this size
150
def load_templates(folder="centered/"):
    templates = {}
    for i in os.listdir(folder):
        champ = i[:-4]
        icon = cv2.imread(folder+i, cv2.IMREAD_GRAYSCALE)
        icon = cv2.resize(icon, (pick_w, pick_h))
        start_x = (pick_w - crop_w) // 2
        start_y = (pick_h - crop_h) // 2
        icon = icon[start_y:start_y + crop_h, start_x:start_x + crop_w]        
        # cv2.imshow("was", icon)
        # cv2.waitKey(0)
        templates[champ] = icon
    return templates

def match_icon(crop, templates):
    crop = cv2.resize(crop, (64, 64))  # Match DDragon size
    best_score = -1
    best_champ = None
    for champ, template in templates.items():
        res = cv2.matchTemplate(crop, template, cv2.TM_CCOEFF_NORMED)
        min_score, max_score, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_score > best_score:
            best_score = max_score
            best_champ = champ
    return best_champ, best_score

def was(w, h):
    return cropped_image[h: h+cropped_height, w: cropped_width]

templates = load_templates()

print("BLUE PICKS:")
for i in blue:
    crop = was(9, i)
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    champ, score = match_icon(crop, templates)
    print(f" -> {champ} (score: {score:.2f})")
    cv2.imshow('Blue Picks', crop)
    cv2.waitKey(0)





# cv2.imwrite('Was.png', cropped_image)
cv2.imshow('Detected Matches', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

