from typing import Union
from .setting import get_params_link, cardPoolType, SupportLang, DefaultColor, NameBanner, ArtBanner, get_color_four_section, get_color_five_section
from .src.tools.uttils import fetch_data
from .src.tools.generator import CardConvene
from .src.tools.model import ConveneData, Calculator

class Convene:
    def __init__(self, link: str) -> None:
        self.data_link = get_params_link(link)

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        pass
    
    async def calculator(self, data: ConveneData, generator: bool = False, art: str = None) -> Calculator:
        total_spin = len(data.data)
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
                "gacha_id": data.gacha_id,
                "card": None
            }
        
        for key in reversed(data.data):
            five_stars += 1
            four_stars += 1
            
            if key.qualityLevel == 5:
                drop = five_stars
                color = await get_color_five_section(drop)
                five_stars = 0
                four_stars = 0
                
                if key.typeRecord == 1:
                    result["info"]["five_stars"]["resonator"] += 1
                else:
                    result["info"]["five_stars"]["weapon"] += 1
                
            elif key.qualityLevel == 4:
                drop = four_stars
                color = await get_color_four_section(drop)
                four_stars = 0
                
                if key.typeRecord == 1:
                    result["info"]["four_stars"]["resonator"] += 1
                else:
                    result["info"]["four_stars"]["weapon"] += 1
            else:
                drop = 1
                color = DefaultColor
                result["info"]["three_stars"]["weapon"] += 1
            
            result["data"].append(
                {
                    "typeRecord": key.typeRecord,
                    "cardPoolType": key.cardPoolType,
                    "resourceId": key.resourceId,
                    "qualityLevel": key.qualityLevel,
                    "resourceType": key.resourceType,
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
            
    async def get(self, gacha_id: Union[int,str], lang: str = "en", generator: bool = False, art: str = None) -> ConveneData:
        """Get information about gacha

        Args:
            gacha_id (Union[int,str]): Id gachi from 1 to 7 (1 - Featured Resonator | 2 - Featured Weapon | 3 - Standard Resonator | 4 - Standard Weapon | 5 - Beginner Convene | 6 - Beginner Convene Choice | 7 - Other)
            lang (str, optional): The language in which to return the result. Defaults to "en" | Acceptable: zh-Hans, zh-Hant, en, ja, ko, fr, de, es 
            generator (bool, optional): Generate a card. Defaults to False.

        Returns:
            BaseModel: ConveneData
        """
        if not lang in SupportLang:
            raise TypeError(f"Argument lang, incorrectly specified, valid values ​​are: {', '.join(SupportLang)}") 
        
        if not str(gacha_id) in cardPoolType:
            raise TypeError("Argument gacha_id, incorrectly specified, valid values ​from 1 to 7 (1 - Featured Resonator | 2 - Featured Weapon | 3 - Standard Resonator | 4 - Standard Weapon | 5 - Beginner Convene | 6 - Beginner Convene Choice | 7 - Other)")
        
        if art is None:
            art = ArtBanner.get(str(gacha_id), "https://i.ibb.co/1XcZSzR/119161444-p0-master1200.jpg")
            
        payload = {
            "playerId": self.data_link.get("player_id"),
            "cardPoolId": self.data_link.get("resources_id"),
            "cardPoolType": int(gacha_id),
            "serverId": self.data_link.get("svr_id"),
            "languageCode": lang,
            "recordId": self.data_link.get("record_id")
        }
                        
        data = ConveneData(**await fetch_data(payload))
        data.gacha_id = int(gacha_id)
        
        if data.code != 0:
            raise TypeError(f"[{data.code}]: {data.message}")
        
        if generator:
            return await self.calculator(data, generator= True, art = art)
        
        return data

        
    