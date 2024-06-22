
# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


DefaultColor = {"hex": "#FFFFFF", "rgba": (255, 255, 255, 255)}

async def get_color_four_section(value):
    if 1 <= value <= 4:
        return {"hex": "#7FFFD4", "rgba": (127, 255, 212, 255)}
    elif 5 <= value <= 7:
        return {"hex": "#FFA500", "rgba": (255, 165, 0, 255)}
    elif 8 <= value <= 10:
        return {"hex": "#8A2BE2", "rgba": (138, 43, 226, 255)}
    
async def get_color_five_section(value):
    if 1 <= value <= 16:
        return {"hex": "#7FFFD4", "rgba": (127, 255, 212, 255)}
    elif 17 <= value <= 32:
        return {"hex": "#FFA500", "rgba": (255, 165, 0, 255)}
    elif 33 <= value <= 48:
        return {"hex": "#8A2BE2", "rgba": (138, 43, 226, 255)}
    elif 49 <= value <= 64:
        return {"hex": "#4682B4", "rgba": (70, 130, 180, 255)}
    elif 65 <= value <= 80:
        return {"hex": "#FF4500", "rgba": (255, 69, 0, 255)}

cardPoolType = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7"
]

SupportLang = [
    "zh-Hans",
    "zh-Hant",
    "en",
    "ja",
    "ko",
    "fr",
    "de",
    "es"
]

ArtBanner = {
    "1": "https://i.ibb.co/fkDnqkK/119017072-p7-master1200.jpg",
    "2": "https://i.ibb.co/YBPp7MQ/119017072-p1-master1200.jpg",
    "3": "https://i.ibb.co/LntsWyK/116174568-p0-master1200.jpg",
    "4": "https://i.ibb.co/fXLbjdS/scar-wuthering-waves-drawn-by-secretfj520-sample-5b5b03239eab755277eb99c116ca38e9.jpg",
    "5": "https://i.ibb.co/px9B0xr/119316451-p0-master1200.jpg",
    "6": "https://i.ibb.co/S33MzKX/119135739-p0-master1200.jpg",
    "7": "https://i.ibb.co/1XcZSzR/119161444-p0-master1200.jpg",
}

NameBanner = {
    "1": "Featured Resonator",
    "2": "Featured Weapon",
    "3": "Standard Resonator",
    "4": "Standard Weapon",
    "5": "Beginner Convene",
    "6": "Beginner Convene Choice",
    "7": "Other Banner",
}

#serverId:
America = "591d6af3a3090d8ea00d8f86cf6d7501"
Asia = "86d52186155b148b5c138ceb41be9650"
Europe = "6eb2a235b30d05efd77bedb5cf60999e"
HMT = "919752ae5ea09c1ced910dd668a63ffb" #(HK, MO, TW)
SEA = "10cd7254d57e58ae560b15d51e34b4c8"


#cardPoolType
FeaturedResonator = "1"
FeaturedWeapon = "2"
StandardResonator = "3"
StandardWeapon = "4"
BeginnerConvene = "5"
BeginnerChoice = "6"
Other = "7"
