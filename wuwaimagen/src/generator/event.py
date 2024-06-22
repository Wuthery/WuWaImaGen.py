from PIL import Image, ImageDraw
from typing import Dict, Union
from datetime import datetime, timedelta
from ..model.event import ActivityItem, GameDatetime
from ..tools.pill import get_font, get_download_img, get_center_size, create_image_with_text
from ..tools.color import get_colors, recolor_image
from ..tools import git

files = git.ImageCache()


class CardEvent:
    def __init__(self, data: ActivityItem):
        self.data = data
        self.today = datetime.now()
        self.one_month_later = self.today + timedelta(days=32)
        
        self.event_pic = []
        self.banner_pic = []
        self.count_event = 0
    
    async def open_recourse(self):
        self.image_line = await files.line
        self.image_line = self.image_line.copy()
        
        self.background = await files.background
        self.background = self.background.copy()
    
    def get_list_data(self, end_date: datetime) -> list:
        current_date = self.today
        date_list = [current_date]
        while current_date <= end_date:
            current_date += timedelta(days=1)
            date_list.append(current_date)
            
            
        return date_list
     
    async def crete_time_line_event(self) -> Dict[str, Union[GameDatetime, str, int]]:
        
        time_line_info = {
            "last_data": self.today,
            "items": []
        }

        for key in self.data:
            time: GameDatetime = key.time()
         
            if time.start.month < self.today.month:
                time.start = time.start.replace(month=self.today.month, day=self.today.day)

            if time.end < self.one_month_later and time.end > time_line_info["last_data"]:
                time_line_info["last_data"] = time.end
                        
            time_line_info["items"].append(
                {
                    "time": time,
                    "name": key.tabTitle.en,
                    "art": key.tabBanner.en[0],
                    "type": 0 if "convene" in key.tabTitle.en.lower() else 1
                }
            )
        
        return time_line_info
    
    async def create_line_banner(self, time_line_info: dict) -> Dict[str, int]:
        
        position = {}
        
        day = self.get_list_data(time_line_info["last_data"])
                    
        spacing = (self.image_line.size[0] - 2 * 25 - len(day) * 51) // (len(day) - 1)
                
        draw = ImageDraw.Draw(self.image_line)
        font = await get_font(40)
        
        x,y = 25,10
        for number in day:
            if self.today.month == number.month:
                draw.text((x, y), str(number.day), font= font, fill=(255,255,255,255))
            else:
                draw.text((x, y), str(number.day), font= font, fill=(255,226,89,255))
            
            
            position[f"{number.day}_{number.month}"] = x
            
            x += 51 + spacing
        
        return position
    
    async def create_icon(self, type: int, art: str) -> Image.Image:

        if type == 0:
            maska = await files.maska_banner
            background = Image.new("RGBA", (325,77), (0,0,0,0))
            icon = await get_download_img(art, size=(325,118))
        else:
            maska = await files.maska_event
            background = Image.new("RGBA", (314,77), (0,0,0,0))
            icon = await get_download_img(art, size=(314,77))
        
        background.paste(icon.convert("RGBA"),(0,0),maska.convert("L"))
        
        return background
        
        
        
    async def add_text_banner(self, name: str, banner: Image.Image) -> Image.Image:
        if banner.size[0] - 200 > 0:
            name = await create_image_with_text(name, 25, banner.size[0] - 330)
            banner.alpha_composite(name,(20,10))
        
        return banner
    
    async def create_banner_event(self,data: dict, position: dict) -> Dict[str, Union[Image.Image, datetime]]:
        line_banner_frame = Image.new("RGBA", (3,77), (255,255,255,255))
        icon = await self.create_icon(data["type"], data["art"])
        color = await get_colors(icon, 15, common=True, radius=5, quality=800)
        
        witch = position["end"] - position["start"]
        
        banner = Image.new("RGBA", (witch, 77), color)

        line_banner_frame, _ = await recolor_image(line_banner_frame, color[:3], light= True)
        
        banner.alpha_composite(line_banner_frame)
        banner.alpha_composite(icon, (witch-icon.size[0],0))
        
        banner = await self.add_text_banner(data["name"], banner)
        
        self.count_event += 1
        
        return {"icon": banner, "start": position["start"]}
    
    
    async def create_background(self, position: dict) -> Image.Image:
        size_hed_up = self.count_event * 83
        card = Image.new("RGBA",(1920, 214 + size_hed_up), (0,0,0,0))
        background_size = await get_center_size((1920, 214 + size_hed_up), self.background)
        card.alpha_composite(background_size)
        card.alpha_composite(self.image_line,(40,25))
        
        line_down = Image.new("RGBA", (1, size_hed_up + 107), (255,255,255,75))
        for x in position:
            card.alpha_composite(line_down,(position[x]+40,91))
        
        return card
    
    async def add_event_banner_icon(self, card: Image.Image) -> Image.Image:
        position_y = 107
        for items in self.banner_pic:
            position_x = items["start"]
            if position_x < 40:
                position_x += 40
            card.alpha_composite(items["icon"], (position_x,position_y))
            position_y += 83
                
        for items in self.event_pic:
            position_x = items["start"]
            if position_x < 40:
                position_x += 40
            card.alpha_composite(items["icon"], (position_x,position_y))
            position_y += 83
        
        return card
    
    
    async def start(self) -> Image.Image:
                
        #Generation setup
        files.set_mapping(2)
        await self.open_recourse()

        #Calculator Convert Data
        time_line_info = await self.crete_time_line_event()
        
        #Start Generation
        position = await self.create_line_banner(time_line_info)
        
        for key in time_line_info["items"]:
            if key["time"].end > time_line_info["last_data"]:
                end_data = f"{time_line_info["last_data"].day}_{time_line_info["last_data"].month}"
            else:
                end_data = f"{key["time"].end.day}_{key["time"].end.month}"
            
            if key["time"].start < self.today:
                start_data = f"{self.today.day}_{self.today.month}"
            else:
                start_data = f"{key["time"].start.day}_{key["time"].start.month}"
            
            position_banner = {
                "start": position.get(start_data),
                "end": position.get(end_data)
            }
            if key["type"] == 0:
                self.banner_pic.append(await self.create_banner_event(key, position_banner))
            else:
                self.event_pic.append(await self.create_banner_event(key, position_banner))
        
        background = await self.create_background(position)        
                                
        return await self.add_event_banner_icon(background)

        