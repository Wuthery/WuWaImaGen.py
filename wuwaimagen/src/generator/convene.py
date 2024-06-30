# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import ImageDraw,Image
from ..tools.pill import get_download_img, get_center_size, get_font, create_image_with_text
from ..tools.color import get_colors, recolor_image
from ..model.convene import Calculator, RecordCalculator
from ..tools import git

files = git.ImageCache()

async def open_background(rank) -> Image.Image:
    if rank == 5:
        return await files.background_five
    elif rank == 4:
        return await files.background_four
    else:
        return await files.background_three
    
async def open_shadow(rank) -> Image.Image:
    if rank == 5:
        return await files.shadow_five
    elif rank == 4:
        return await files.shadow_four
    else:
        return await files.shadow_three


async def get_stars(rank) -> Image.Image:
    if rank == 5:
        return await files.five_stars
    elif rank == 4:
        return await files.four_stars
    else:
        return await files.three_stars
        

class CardConvene:
    def __init__(self, data: Calculator, name_banner: str = "Other Banner"):
        self.data = data 
        self.name_banner = name_banner
        
    async def create_art(self, art: Image.Image):
        self.background = Image.new("RGBA", (330,599), (0,0,0,0))
        self.background.alpha_composite(art,(-68,0))
        
    async def create_count(self,value: int, color: tuple) -> Image.Image:
        background = await files.count
        background = background.copy()
        line = await files.count_line
        color_line = await files.count_color_line
        color_line = await recolor_image(color_line.copy(), color[:3])
        
        background.alpha_composite(color_line)
        background.alpha_composite(line)
        
        d = ImageDraw.Draw(background)
            
        font = await get_font(40)
        x = int(font.getlength(str(value))/2)
        d.text((46-x,26), str(value), font= font, fill=(255, 255, 255, 255))
        
        return background
        
    async def create_icons(self, data: RecordCalculator) -> Image.Image:
        background = await open_background(data.qualityLevel)
        background = background.copy()
        shadow = await open_shadow(data.qualityLevel)

        icon = await data.get_icon()
        if data.typeRecord == 1:
            icon = await get_download_img(icon.banner, size= (798,1100))
            background.alpha_composite(icon,(-100,-124))
        else:
            icon = await get_download_img(icon.icon, size= (414,414))
            background.alpha_composite(icon,(0,63))
        
        background.alpha_composite(shadow)
        
        count = await self.create_count(data.drop, data.color.rgba)
        background.alpha_composite(count,(325,386))
        
        stars = await get_stars(data.qualityLevel)
        background.alpha_composite(stars.resize((143,32)),(7,442))
        
        name = await create_image_with_text(data.name, 40, max_width=388, color=(255, 255, 255, 255))
        background.alpha_composite(name, (int(208-name.size[0]/2), int(520-name.size[1]/2)))
        
        return {"icon": background, "rarity": data.qualityLevel}

    async def build(self, color: tuple) -> Image.Image:
        frame = await files.frame
        background = Image.new("RGBA", (1065,599), color)
        background.alpha_composite(frame)
        background.alpha_composite(self.background)
        line = await files.line
        line, _ = await recolor_image(line.copy(), color, light = True)
        background.alpha_composite(line)
        
        position_x = 353
        position_y = 69
        
        for _, key in enumerate(reversed(self.icon)):
            if _ in [5,10]:
                position_y += 177
                position_x = 353
            background.alpha_composite(key["icon"].resize((115,158)),(position_x,position_y))
            
            position_x += 146
        
        name = await create_image_with_text(self.name_banner, 20, max_width=217, color=(255, 255, 255, 255))
        
        background.alpha_composite(name,(353,15))
        
        d = ImageDraw.Draw(background)
        font = await get_font(21)
        d.text((589,17), f"Total: {self.data.info.total_spin}", font= font, fill=(255, 255, 255, 255))
        d.text((792,17), f"5: {self.data.info.next.five}/80", font= font, fill=(255, 255, 255, 255))
        d.text((945,17), f"4: {self.data.info.next.four}/10", font= font, fill=(255, 255, 255, 255))
        
        return background
        
    async def start(self, art: str) -> Image.Image:
        
        files.set_mapping(1)
        
        art = await get_download_img(art)
        art = await get_center_size((466,600), art)
        color = await get_colors(art, 15, common=True, radius=5, quality=800)
            
        await self.create_art(art)

        self.icon = []
        i = 1
        for key in reversed(self.data.data):
            if i == 15:
                break
            
            if key.qualityLevel > 3:
                self.icon.append(await self.create_icons(key))
                i += 1
                
        return await self.build(color)