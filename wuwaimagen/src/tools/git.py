# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image
import os
import cachetools
import threading
from pathlib import Path
from io import BytesIO
from .http import AioSession
from ..settings.other import assets_local
lock = threading.Lock()

_caches = cachetools.TTLCache(maxsize=1000, ttl=300)  

_BASE_URL = 'https://raw.githubusercontent.com/Wuthery/WuWaImaGen.py/main/assets/'

total_style = {
    'five_stars': 'stars/five.png',
    'four_stars': 'stars/four.png',
    'three_stars': 'stars/three.png',
    'two_stars': 'stars/two.png',
    'one_stars': 'stars/one.png',
    
    't_five_stars': 'stars/t_stars_five.png',
    't_four_stars': 'stars/t_stars_four.png',
    't_three_stars': 'stars/t_stars_three.png',
    't_two_stars': 'stars/t_stars_two.png',
    't_one_stars': 'stars/t_stars_one.png',
}


map_conve = {
    'line': 'convene/line.png',
    'frame': 'convene/frame.png',
    'maska': 'convene/maska.png',
    
    'background_five': 'convene/character/background_five.png',
    'background_four': 'convene/character/background_four.png',
    'background_three': 'convene/character/background_three.png',
    
    'shadow_five': 'convene/character/shadow_five.png',
    'shadow_four': 'convene/character/shadow_four.png',
    'shadow_three': 'convene/character/shadow_three.png',
    
    'count_color_line': 'convene/character/count_color_line.png',
    'count_line': 'convene/character/count_line.png',
    'count': 'convene/character/count.png',
    
    
}

map_event = {
    'background': 'event/background.png',
    'line': 'event/data_line.png',
    'maska_banner': 'event/maska_banner.png',
    
    'maska_info_banner': 'event/maska_info_banner.png',
    'maska_left': 'event/maska_left.png',
    'maska_right': 'event/maska_right.png',
    'maska_banner': 'event/maska_banner.png',
    'maska_event': 'event/maska_event.png'
    
}


map_business_card = {
    'background': 'business_card/background.png',
    'element_dark': 'business_card/element/Dark.png',
    'element_fire': 'business_card/element/Fire.png',
    'element_ice': 'business_card/element/Ice.png',
    'element_light': 'business_card/element/Light.png',
    'element_thunder': 'business_card/element/Thunder.png',
    'element_wind': 'business_card/element/Wind.png',
    'maska': 'business_card/element/maska.png',
}


map_matterial_card = {
    'background': 'matterial/character/background.png',
    'five_background': 'matterial/character/five_background.png',
    'four_background': 'matterial/character/four_background.png',
    'frame': 'matterial/character/frame.png',

    'background_element_dark': 'matterial/character/dark.png',
    'background_element_fire': 'matterial/character/fire.png',
    'background_element_ice': 'matterial/character/ice.png',
    'background_element_light': 'matterial/character/light.png',
    'background_element_thunder': 'matterial/character/thunder.png',
    'background_element_wind': 'matterial/character/wind.png',
    
    'items_one': 'matterial/items/one.png',
    'items_two': 'matterial/items/two.png',
    'items_three': 'matterial/items/three.png',
    'items_four': 'matterial/items/four.png',
    'items_five': 'matterial/items/five.png',
    
    'background_five': 'matterial/weapon/background_five.png',
    'background_four': 'matterial/weapon/background_four.png',
    'background_three': 'matterial/weapon/background_three.png',
    'background_two': 'matterial/weapon/background_two.png',
    'background_one': 'matterial/weapon/background_one.png',
    
    'mask': 'matterial/weapon/mask.png',
    
}
map_weapon_card = {
    'maska_weapon': 'wiki/weapon/maska_weapon.png',
    'background': 'wiki/weapon/WeaponBackground.png',
    
    'items_five': 'wiki//weapon/frame_items/five.png',
    'items_four': 'wiki//weapon/frame_items/four.png',
    'items_three': 'wiki//weapon/frame_items/three.png',
    'items_two': 'wiki//weapon/frame_items/two.png',
    'items_one': 'wiki//weapon/frame_items/one.png',
    
    'character_background': 'wiki//character/character_background.png',
    'character_constant': 'wiki//character/constant.png',
    'character_food_background': 'wiki//character/foodbackground.png',
    'character_level_frame': 'wiki//character/level_frame.png',
    'character_line': 'wiki//character/line.png',
    'character_skill_frame': 'wiki//character/skill_frame.png',
    'character_skill_stat': 'wiki//character/skill_stat.png',
    'character_ascension_line': 'wiki//character/ascension_line.png',

    
}
    
class ImageCache:
    
    _assets_download = False
    _mapping = {}
            
    @classmethod
    async def set_assets_download(cls, download = False):
        cls._assets_download = download
    
    @classmethod
    def set_mapping(cls,mod):
        if mod == 1:
            cls._mapping = map_conve
        elif mod == 2:
            cls._mapping = map_event
        elif mod == 3:
            cls._mapping = map_business_card
        elif mod == 4:
            cls._mapping = map_matterial_card
        elif mod == 5:
            cls._mapping = map_weapon_card
        
    @classmethod
    async def _load_image(cls, name) -> Image.Image:
        
        try:
            image = _caches[name]
        except KeyError:
            try:
                _caches[name] = image = Image.open(assets_local / name)
                return _caches[name]
            except Exception as e:
                pass
        
        try:
            _caches[name] = image = Image.open(assets_local / name)
            return _caches[name]
        except Exception as e:
            pass
        
        url = _BASE_URL + name
        if url in _caches:
            return _caches[name]
        else:
            image_data = await AioSession.get(url, response_format= "bytes")
            image = Image.open(BytesIO(image_data))
            _caches[name] = image
        
        if cls._assets_download:
            file_path = assets_local / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(str(assets_local / name))
        
        return image

    def __getattr__(cls, name) -> Image.Image:
        if name in cls._mapping:
            return cls._load_image(cls._mapping[name])
        else:
            if name in total_style:
                return cls._load_image(total_style[name]) 
            else:
                raise AttributeError(f"'{cls.__class__.__name__}' object has no attribute '{name}'")