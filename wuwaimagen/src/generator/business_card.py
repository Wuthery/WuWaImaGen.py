# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import asyncio
from typing import Union, List
from PIL import ImageDraw,Image
from ..tools.pill import get_download_img, get_center_size, get_font, create_image_with_text
from ..tools.color import get_colors, recolor_image
from ..model.business_card import Config
from ..tools import git, utils
from ..settings.other import WUTHERY_CDN
files = git.ImageCache()


'''async def open_background_element(element_id):
    if element_id == 6:
        return await files.element_dark
    elif element_id == 5:
        return await files.element_light
    elif element_id == 4:
        return await files.element_wind
    elif element_id == 3:
        return await files.element_thunder
    elif element_id == 2:
        return await files.element_fire
    else:
        return await files.element_ice'''
        
async def open_background_element(element_id: int) -> Image.Image:
    elements = {
        6: lambda: files.element_dark,
        5: lambda: files.element_light,
        4: lambda: files.element_wind,
        3: lambda: files.element_thunder,
        2: lambda: files.element_fire,
        1: lambda: files.element_ice
    }
    element_func = elements.get(element_id, lambda: files.element_ice)
    return await element_func()
    

class CardConvene:
    def __init__(self, data: Config):
        self.data = data
    
    async def create_icon(self, resonator_id: Union[str,int], element: int, icon: str):
        
        user_art = False
        if not self.data.resonator_art is None:
            resonator_id_str = str(resonator_id)
            if resonator_id_str in self.data.resonator_art:
                icon = self.data.resonator_art.get(resonator_id_str)
                user_art = True
            if int(resonator_id) in self.data.resonator_art:
                icon = self.data.resonator_art.get(int(resonator_id))
                user_art = True
        
        
        icon_size = (390, 460) if user_art else (333, 457)
        icon = await get_download_img(icon, size=icon_size if not user_art else None)
        if user_art:
            icon = await get_center_size((390, 460), icon)
        
        maska = await files.maska
        
        background = Image.new("RGBA", (230,460),(0,0,0,0))
        background_mask = Image.new("RGBA", (230,460),(0,0,0,0))
        
        offset_x = -69 if user_art else -44
        background_mask.alpha_composite(icon, (offset_x, 0))
        background.paste(background_mask, (0, 0), maska.convert("L"))

        background_element = await open_background_element(element)
        background_element = background_element.copy()

        background_element.alpha_composite(background)
        
        return background_element
    
    async def create_screenshot(self):
        if self.data.screenshot is None:
            return Image.new("RGBA", (1,1), (0,0,0,0))
        
        icon = await get_download_img(self.data.screenshot)

        return await get_center_size((370,300), icon)
    
    async def create_background(self, icon: List[Image.Image], screenshot: Image.Image,):
        background: Image.Image = await files.background
        background = background.copy().convert("RGBA")
        
        position = 75
        for key in icon:
            background.alpha_composite(key,(position,162))
            position += 260
                
        texts = [
            (str(self.data.nickname), 258, 30, 299),
            (str(self.data.uid), 258, 30, 299),
            (str(self.data.level), 258, 30, 299),
            (str(self.data.play_style), 258, 20, 299),
            (str(self.data.signature), 450, 30, 1018)
        ]
        
        y_positions = [680, 764, 853, 943, 1018]
        
        for (text, x_p, font_size, max_width), y_pos in zip(texts, y_positions):
            img_text = await create_image_with_text(text, font_size, max_width, (207, 186, 119, 255))
            x = x_p - img_text.width // 2
            background.alpha_composite(img_text, (x, y_pos))

        background.alpha_composite(screenshot, (460, 677))
        return background
    
    async def start(self) -> Image.Image:
        
        files.set_mapping(3)
        
        items = await utils.get_open_file()

        reloading = True
        icon_list = []
        
        for key in self.data.resonator:
            data = next(filter(lambda x: x["Id"] == int(key), items), None)
            if data is None and reloading:
                items = await utils.get_data_resonator()
                data = next(filter(lambda x: x["Id"] == key, items), None)
                reloading = False
             
            if data is None:
                continue
            
            element_id = data.get("ElementId", 1)
            icon =  WUTHERY_CDN + f"p/GameData/IDFiedResources/Common/Image/IconRolePile/{data["Id"]}.png"
            
            icon_list.append(await self.create_icon(data["Id"],element_id,icon))
        
        screenshot = await self.create_screenshot() 
        result = await self.create_background(icon_list, screenshot)
        
        return result
            
        