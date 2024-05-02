from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from decimal import Decimal
from utils.ei import get_first_contact
from utils import tools as t
# TODO: Add ultra pro/standard
import json


def genImages():
    print("making images")
    # Config Shit
    img_width = 480
    img_height = 320
    font_lg = ImageFont.truetype("assets/fonts/always-together.ttf", 40)
    font_med = ImageFont.truetype("assets/fonts/always-together.ttf", 30)
    font_sm = ImageFont.truetype("assets/fonts/always-together.ttf", 20)
    backup = get_first_contact("EI5450109629759488")
    with open("assets/eggs.json") as eggJson:
        eggList = json.load(eggJson)


    # Create the new image
    im = Image.new(
        mode = "RGB", 
        size = (img_width, img_height),
        color = (153, 153, 255))
    draw = ImageDraw.Draw(im)
    
    # Add username
    draw.text((img_width/2,img_height/15*2 + 2), f'{backup["backup"]["userName"]}', fill="black", font=font_lg, anchor="ms")
    # Get all needed info for eb
    ebData = t.get_earning_bonus_data(backup)
    eb = t.calculate_earning_bonus(ebData["sE"], ebData["pE"], ebData["pB"], ebData["sF"], False)
    currentRank = t.get_order_of_magnitude_rank(eb)
    eb = t.human_format(eb)
    # Add eb% 3/4 of the way down the screen, centered
    draw.text((img_width/2,img_height/10*8), f"{eb}%", fill="black", font=font_med, anchor="ms")
    # Add current rank 7/8 of the way down the screen, centered
    draw.text((img_width/2,img_height/10*9), f"{currentRank}", fill="black", font=font_med, anchor="ms")
    
    # Add Soul Egg Count
    soulEggImage = Image.open("assets/images/misc/currency/egg_soul.png")
    soulEggImage.thumbnail((32, 32))
    im.paste(soulEggImage, ((5, 5)), soulEggImage)
    draw.text((37, 12), f'{t.human_format(Decimal(ebData["sE"]))}', fill="black", font=font_med)
    
    # Add Prophecy Egg Count
    prophecyEggImage = Image.open("assets/images/misc/currency/egg_of_prophecy.png")
    prophecyEggImage.thumbnail((32, 32))
    im.paste(prophecyEggImage, ((5, 40)), prophecyEggImage)
    draw.text((37, 47), f'{ebData["pE"]}', fill="black", font=font_med)
    
    # Add Golden Egg Count
    goldenEggImage = Image.open("assets/images/misc/currency/golden_egg.png")
    goldenEggImage.thumbnail((32, 32))
    im.paste(goldenEggImage, ((5, 75)), goldenEggImage)
    ge = int(backup["backup"]["game"]["goldenEggsEarned"]) - int(backup["backup"]["game"]["goldenEggsSpent"])
    draw.text((37, 80), f"{t.human_format(ge)}", fill="black", font=font_med)

    
    
    
    
    
    # Get current home farm and format image
    for farm in backup["backup"]["farms"]:
        if farm["farmType"] == "HOME":
            currentEggImage = Image.open(eggList[farm["eggType"]]["imageLocation"]) # 256 x 256
            currentEggImage.thumbnail((200, 200))
    # Add the current egg image, centered but raised 40 px
    im.paste(currentEggImage, (((img_width-currentEggImage.width)//2),((img_height-currentEggImage.height)//2) - 25), currentEggImage)
    
    # Check pro permit status
    if backup["backup"]["game"]["permitLevel"] == 1:
        permitImageSrc = "assets/images/misc/permit/pro_permit.png"
    else: permitImageSrc = "assets/images/misc/permit/free_permit.png"
    permitImage = Image.open(permitImageSrc) # 300 x 200
    permitImage.thumbnail((75,50))
    # Add the Permit Image
    im.paste(permitImage, (round(img_width/6*5), 5), permitImage)
    
    
    try:
        im.save("assets/output/home.png", "PNG")
    except IOError as e:
        print(e)
    
    
    