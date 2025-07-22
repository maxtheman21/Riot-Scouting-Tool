import cv2
import numpy as np
import os

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




pick_w, pick_h = 535, 300 # resize the pick image to this size and then
crop_w, crop_h = 220, 105 # crop the *center* to this size

def load_picks(folder="centered/"):
    templates = {}
    for i in os.listdir(folder):
        champ = i[:-4]
        icon = cv2.imread(folder+i, cv2.IMREAD_GRAYSCALE)
        icon = cv2.resize(icon, (pick_w, pick_h))
        start_x = (pick_w - crop_w - 10) // 2
        start_y = (pick_h - crop_h - 90) // 2
        icon = icon[start_y:start_y + crop_h, start_x:start_x + crop_w]        
        templates[champ] = icon
    return templates

templates = load_picks()

pick_w, pick_h = 318, 179 # resize the pick image to this size and then
crop_w, crop_h = 63, 95 # crop the *center* to this size

def load_bans(folder="centered/"):
    templates = {}
    for i in os.listdir(folder):
        champ = i[:-4]
        icon = cv2.imread(folder+i, cv2.IMREAD_GRAYSCALE)
        icon = cv2.resize(icon, (pick_w, pick_h))
        start_x = (pick_w - crop_w - 10) // 2
        start_y = (pick_h - crop_h - 50) // 2
        icon = icon[start_y:start_y + crop_h, start_x:start_x + crop_w]        
        templates[champ] = icon
        # cv2.imshow("was", icon)
        # cv2.waitKey(0)
    return templates

template = load_bans()

def match_icon(crop, templates):
    best_score = -1
    best_champ = None
    for champ, template in templates.items():
        res = cv2.matchTemplate(crop, template, cv2.TM_CCOEFF_NORMED)
        min_score, max_score, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_score > best_score:
            best_score = max_score
            best_champ = champ
    return best_champ, best_score


picks = [52, 165, 277, 423, 535] # 232 & 1326
bans = [27, 117, 207, 347, 437, 844, 934, 1074, 1164, 1254] # 650

print("BLUE PICKS:")
for i in picks:
    crop = cropped_image[i: i+107, 9: 9+223] # 232
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    champ, score = match_icon(crop, templates)
    print(champ)

print("RED PICKS:")
for i in picks:
    crop = cropped_image[i: i+107, 1103: 1103+223]  # 1326
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    champ, score = match_icon(crop, templates)
    print(champ)

print ("BANS:")
for i in bans:
    crop = cropped_image[650: 650 + 85, i: i + 53]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    champ, score = match_icon(crop, template)    
    print(champ)

cv2.imshow('Detected Matches', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

