# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import kuro
from typing import Union
from ..settings.convene import  cardPoolType, SupportLang, DefaultColor, NameBanner, ArtBanner, get_color_four_section, get_color_five_section
from ...src.generator.convene import CardConvene
from ...src.model.convene import Calculator
from .main import MainWuWaImaGen
from ..tools import git
from kuro.utility.gacha import parse_gacha_url

client = kuro.Client()

class ConveneClient(MainWuWaImaGen):
        
    async def get_gacha_info(self, link: str, gacha_id: Union[int,str] = None, lang: str = "en", generator: bool = False, art: str = None) -> Calculator:
        """Gacha counting

        Args:
            link (str): Story Log Link.
            gacha_id (Union[int,str], optional): Id gacha_id from 1 to 7 (1 - Featured Resonator | 2 - Featured Weapon | 3 - Standard Resonator | 4 - Standard Weapon | 5 - Beginner Convene | 6 - Beginner Convene Choice | 7 - Other)
            lang (str, optional): The language in which to return the result. Defaults to "en" | Acceptable: zh-Hans, zh-Hant, en, ja, ko, fr, de, es 
            generator (bool, optional): Generate a card or not. Defaults to False.
            art (str, optional): Custom image, if empty will be selected from the standard ones. Defaults to None.

        Returns:
            Calculator: BaseModel
        """
        
        await git.ImageCache.set_assets_download(self.assets)
        
        if not lang in SupportLang:
            raise TypeError(f"Argument lang, incorrectly specified, valid values ​​are: {', '.join(SupportLang)}") 
        
        if not str(gacha_id) in cardPoolType:
            raise TypeError("Argument gacha_id, incorrectly specified, valid values ​from 1 to 7 (1 - Featured Resonator | 2 - Featured Weapon | 3 - Standard Resonator | 4 - Standard Weapon | 5 - Beginner Convene | 6 - Beginner Convene Choice | 7 - Other)")
        
        parse = parse_gacha_url(link)
        if not gacha_id is None:
            parse["banner"] = kuro.types.WuWaBanner(int(gacha_id))
        
        if not lang is None:
            parse["lang"] = kuro.types.Lang(lang)
            
        data_convene = await client.get_gacha_record(**parse)
        
        total_spin = len(data_convene)
        five_stars = 0
        four_stars = 0

        
        result = {"info": {
            "total_spin": total_spin,
            "astrite": total_spin * 160,
            "next": {"five": 80, "four": 10},
            "five_stars": {"resonator": 0, "weapon": 0},
            "four_stars": {"resonator": 0, "weapon": 0},
            "three_stars": {"resonator": 0, "weapon": 0}
            },
                "data": [],
                "gacha_id": parse["banner"],
                "card": None
            }
        
        for key in reversed(data_convene):
            five_stars += 1
            four_stars += 1
            
            if key.rarity == 5:
                drop = five_stars
                color = await get_color_five_section(drop)
                five_stars = 0
                four_stars = 0
                
                if key.type == 1:
                    result["info"]["five_stars"]["resonator"] += 1
                else:
                    result["info"]["five_stars"]["weapon"] += 1
                
            elif key.rarity == 4:
                drop = four_stars
                color = await get_color_four_section(drop)
                four_stars = 0
                
                if key.type == 1:
                    result["info"]["four_stars"]["resonator"] += 1
                else:
                    result["info"]["four_stars"]["weapon"] += 1
            else:
                drop = 1
                color = DefaultColor
                result["info"]["three_stars"]["weapon"] += 1
            
            result["data"].append(
                {
                    "typeRecord": key.type,
                    "cardPoolType": key.banner,
                    "resourceId": key.resource_id,
                    "qualityLevel": key.rarity,
                    "resourceType": key.type_name,
                    "name": key.name,
                    "count": key.count,
                    "time": key.time,
                    "drop": drop,
                    "color": color
                })
        
        result["info"]["next"]["five"] -= five_stars
        result["info"]["next"]["four"] -= four_stars
        
        data = Calculator(**result)
        
        if art is None:
            art = ArtBanner.get(str(data.gacha_id), "https://i.ibb.co/1XcZSzR/119161444-p0-master1200.jpg")
        
        if generator:
            data.card = await CardConvene(data, name_banner= NameBanner.get(str(data.gacha_id), "Other Banner")).start(art)
        
        return data
