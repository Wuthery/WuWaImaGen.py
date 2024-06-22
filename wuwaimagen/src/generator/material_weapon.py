# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from typing import  List
from PIL import ImageDraw,Image
from ..tools.pill import get_download_img, get_center_size, get_font, create_image_with_text
from ..model.material import CalculatorMaterialModel, Material, Level
from ..tools import git

files = git.ImageCache()

async def open_background_rarity(rarity: int) -> Image.Image:
    elements = {
        5: lambda: files.background_five,
        4: lambda: files.background_four,
        3: lambda: files.background_three,
        2: lambda: files.background_two,
        1: lambda: files.background_one
    }
    element_func = elements.get(rarity, lambda: files.background_one)
    return await element_func()


async def open_background_items_rarity(rarity: int) -> Image.Image:
    elements = {
        5: lambda: files.items_five,
        4: lambda: files.items_four,
        3: lambda: files.items_three,
        2: lambda: files.items_two,
        1: lambda: files.items_one
    }
    element_func = elements.get(rarity, lambda: files.items_one)
    return await element_func()

color_rarity = {
    5: (207,155,45,255),
    4: (137,55,198,255),
    3: (21,96,196,255),
    2: (0,195,118,255),
    1: (75,75,75,255),
}

class CardWeaponMaterial:
    def __init__(self, data: CalculatorMaterialModel):
        self.data = data
    
    async def create_icon_weapon(self) -> Image.Image:
        mask: Image.Image = await files.mask
        icon = await get_download_img(self.data.weapon.icon, size= (235,235))
        background_icon = Image.new("RGBA", (235,235), color= (0,0,0,0))
        background_icon.paste(icon,(0,0), mask.convert("L"))
                
        return background_icon
    
    async def create_icon_items(self, items: Material) -> Image.Image:
        icon = await get_download_img(items.icon, size=(112,112))
        background = await open_background_items_rarity(items.rarity)
        background_icon = background.copy()
        background_icon.alpha_composite(icon, (0,0))
        
        value = await create_image_with_text(str(items.value), 18, max_width= 102, color=(255,255,255,255))
        
        background_icon.alpha_composite(value, (62 - (int(value.width/2)),115))
        
        return background_icon
    
    async def start(self, level: Level) -> Image.Image:
        files.set_mapping(4)
        
        icon = await self.create_icon_weapon()
        
        background = await open_background_rarity(self.data.weapon.rarity)
        background = background.copy()

        background.alpha_composite(icon,(151,155))
        
        icon_money = False
        if len(self.data.items) > 8:
            icon_money = True
            
        x = 9
        y = 442
        i = 0
        for key in self.data.items:
            items_icon = await self.create_icon_items(self.data.items.get(key))
            if icon_money:
                background.alpha_composite(items_icon, (9, 296))
                icon_money = False
                continue
            
            background.alpha_composite(items_icon, (x, y))
            
            x += 135
            i += 1
            
            if i == 4:
                x = 9
                y += 170
        
        color = color_rarity.get(self.data.weapon.rarity, (0,0,0,255))                
        name = await create_image_with_text(self.data.weapon.name, 35, 524, color)
        level = await create_image_with_text(f"Level: {level.max}", 35, 277, color)
        
        background.alpha_composite(name, (269 - int(name.width/2),99))
        background.alpha_composite(level, (269 - int(level.width/2),400))
                
        return background