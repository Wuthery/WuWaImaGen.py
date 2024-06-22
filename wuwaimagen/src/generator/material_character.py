# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from typing import  List
from PIL import ImageDraw,Image
from ..tools.pill import get_download_img, get_center_size, get_font, create_image_with_text
from ..model.material import CalculatorMaterialModel, Material, Level
from ..tools import git

files = git.ImageCache()

async def open_stars(rarity: int) -> Image.Image:
    elements = {
        5: lambda: files.five_stars,
        4: lambda: files.four_stars
    }
    element_func = elements.get(rarity, lambda: files.four_stars)
    return await element_func()


async def open_background_rarity(rarity: int) -> Image.Image:
    elements = {
        5: lambda: files.five_background,
        4: lambda: files.four_background
    }
    element_func = elements.get(rarity, lambda: files.four_background)
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

async def open_shadow_element(element_id: int) -> Image.Image:
    elements = {
        6: lambda: files.background_element_dark,
        5: lambda: files.background_element_light,
        4: lambda: files.background_element_wind,
        3: lambda: files.background_element_thunder,
        2: lambda: files.background_element_fire,
        1: lambda: files.background_element_ice
    }
    element_func = elements.get(element_id, lambda: files.background_element_ice)
    return await element_func()
    

class CardCharacterMaterial:
    def __init__(self, data: CalculatorMaterialModel):
        self.data = data
    
    async def create_background(self):
        background = await files.background
        self.background: Image.Image = background.copy()

        shadow = await open_shadow_element(self.data.character.element_id)
        self.background.alpha_composite(shadow)
        
        background = await open_background_rarity(self.data.character.rarity)
        self.background.alpha_composite(background, (130,24))

        icon = await get_download_img(self.data.character.banner, size=(357,520))
        self.background.alpha_composite(icon, (32,56))
        
        frame = await files.frame
        self.background.alpha_composite(frame)
    
    async def create_icon_items(self, items: Material) -> Image.Image:
        icon = await get_download_img(items.icon, size=(112,112))
        background = await open_background_items_rarity(items.rarity)
        background_icon = background.copy()
        background_icon.alpha_composite(icon, (0,0))
        
        value = await create_image_with_text(str(items.value), 18, max_width= 102, color=(255,255,255,255))
        
        background_icon.alpha_composite(value, (62 - (int(value.width/2)),115))
        
        return background_icon
    
    async def create_name(self) -> Image.Image:
        name_icon = Image.new("RGBA", (339,85), (0,0,0,0))
        stars = await open_stars(self.data.character.rarity)
        stars = stars.resize((122,28))
        name = await create_image_with_text(self.data.character.name, 35, 337, (255,255,255,255))

        x = 336 - name.width
        name_icon.alpha_composite(name, (x, 6))
        y = name.height
        if y > 36:
            y = 36 + 12
            
        name_icon.alpha_composite(stars, (336 - stars.width, y))
        
        return name_icon
    
    
    async def start(self, level: Level) -> Image.Image:
        files.set_mapping(4)
        
        await self.create_background()
        
        
        x = 438
        y = 63
        for i, key in  enumerate(self.data.items, start= 1):
            items_icon = await self.create_icon_items(self.data.items.get(key))
            
            if i in [5,9]:
                x = 438
                y += 168

            self.background.alpha_composite(items_icon, (x, y))
            
            x += 146
        
        name = await self.create_name()
        
        self.background.alpha_composite(name, (49,484)) 
        
        
        draw = ImageDraw.Draw(self.background)
        font = await get_font(24)
        draw.text((634,32), f"Level: {level.min} - {level.max}", font = font, fill = (255,255,255,255))
        
        return self.background
        
        
        
        
        
        