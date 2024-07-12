from typing import  List
from PIL import ImageDraw,Image
from ..tools.pill import get_download_img, get_center_size, get_font, create_image_with_text, apply_opacity, create_image_with_text_v2
from ..model.wiki import WikiWeapon, StatsWeaponInfo, WikiCharacter
from ..tools import git, utils

files = git.ImageCache()



async def get_stars(rarity:int):
    stars = {
        5: lambda: files.t_five_stars,
        4: lambda: files.t_four_stars,
        3: lambda: files.t_three_stars,
        2: lambda: files.t_two_stars,
        1: lambda: files.t_one_stars
    }
    stars_func = stars.get(rarity, lambda: files.t_one_stars)
    return await stars_func()

async def get_frame_items(rarity:int):
    frame = {
        5: lambda: files.items_five,
        4: lambda: files.items_four,
        3: lambda: files.items_three,
        2: lambda: files.items_two,
        1: lambda: files.items_one
    }
    frame_func = frame.get(rarity, lambda: files.items_one)
    return await frame_func()


def apply_params_to_effect(effect: str, params: dict, level: int) -> str:

    
    values = [params[str(i)][level] for i in range(len(params))]
    try:
        return effect.format(*values)
    except:
        values.append(values[len(values)-1])
        values.append(values[len(values)-1])
        print(values)
        return effect.format(*values)

class WikiWeaponCard:
    def __init__(self, data: WikiWeapon, lang: str = "en"):
        self.data = data
        self.lang = lang
        
        
    
    async def create_line_stat(self, info: StatsWeaponInfo):
        line = Image.new("RGBA", (160,40), (0,0,0,0))
        icon = await get_download_img(info.icon, size=(40,40))
        line.alpha_composite(icon)
        
        draw = ImageDraw.Draw(line)
        font = await get_font(23)
        value = int(info.value)
        
        if info.is_ration:
            value = f"{round(info.value * 100, 1)}%"
        
        
        draw.text((45,11), str(value), font = font, fill = (255,255,255,255))
        
        
        return line
    
    
    async def create_items_icon(self, id: int, value: int):
        
        data = await utils.get_open_file(f"grouped/{self.lang}/items/{id}.json")
        if data == {}:
            data =  await utils.get_data(self.lang, catalog = "items", filename = str(id))
            
        
        background = Image.new("RGBA", (138,161), (0,0,0,0))
        frame = await get_frame_items(data.get("rarity").get("id"))
        icon = await get_download_img(data.get("icon").get("icon"), size=(112,112))
        background.alpha_composite(icon, (13,13))
        background.alpha_composite(frame)
        
        draw = ImageDraw.Draw(background)
        font = await get_font(22)
        x = int(font.getlength(str(value))/2)
        draw.text((69-x,141), str(value), font = font, fill = (255,255,255,255))
        
        
        return {"id": id, "icon": background}
    
    async def create_items(self):
        
        items_l = {}
        
        for key in self.data.ascensions:
            for items in self.data.ascensions[key]:
                if not items in items_l:
                    items_l[items] = self.data.ascensions[key][items]
                else:
                    items_l[items] += self.data.ascensions[key][items]
        
        icon = []
        items_l = utils.sort_items(items_l)
        for key in items_l:
            icon.append(await self.create_items_icon(key, items_l[key]))
        
        return icon
    
    async def create_left_page(self):
        background = Image.new("RGBA", (1328,1328), (0,0,0,0))
        mask = await files.maska_weapon
        
        background_icon = Image.new("RGBA", (322,321), (0,0,0,0))
        icon = await get_download_img(self.data.icon.icon, size=(322,321))
        
        background_icon.paste(icon,(0,0), mask.convert("L"))
        
        background.alpha_composite(background_icon,(165,463))
        
        weapon_type_icon = await get_download_img(self.data.type.icon, size=(128,128))
        
        background.alpha_composite(weapon_type_icon,(506,458))
                
        stats_level_min = await self.create_line_stat(self.data.stats.get("first"))
        stats_level_max = await self.create_line_stat(self.data.stats.get("second"))
        
        background.alpha_composite(stats_level_min,(25,855))
        background.alpha_composite(stats_level_max,(25,905))
        
        
        stats_level_min = await self.create_line_stat(self.data.stats_level.get("6").get("90")[0])
        stats_level_max = await self.create_line_stat(self.data.stats_level.get("6").get("90")[1])
        
        background.alpha_composite(stats_level_min,(508,855))
        background.alpha_composite(stats_level_max,(508,905))
        
        desc = await create_image_with_text_v2(self.data.description, 17, max_width=625, color=(255, 255, 255, 255))
        background.alpha_composite(desc,(22,1070))
        
        name_shadow_background = Image.new("RGBA", (662,451), (0,0,0,0))
        
        name_shadow = await create_image_with_text(self.data.name, 136, max_width=995, color=(255, 255, 255, 20))
        name_shadow_background.alpha_composite(name_shadow)
        background.alpha_composite(name_shadow_background,(0,77))
        
        name_white = await create_image_with_text(self.data.name, 82, max_width=603, color=(255, 255, 255, 255))
        background.alpha_composite(name_white,(23,123))
        
        
        stars = await get_stars(self.data.rarity.id)
        background.alpha_composite(stars,(23,627))
        
        
        draw = ImageDraw.Draw(background)
        font = await get_font(54)
        x = int(font.getlength(str(self.data.rarity.name))/2)
        draw.text((80-x,546), str(self.data.rarity.name), font = font, fill = (255,211,125,255))
        
        font = await get_font(25)
        x = int(font.getlength(f"ID: {self.data.id}")/2)
        draw.text((576-x,634), f"ID: {self.data.id}", font = font, fill = (255,211,125,255))
        
        return background
    
    async def create_right_page(self):
        background = Image.new("RGBA", (1328,1328), (0,0,0,0))
        
        weapon_type_icon = await get_download_img(self.data.type.icon, size=(658,659))
        weapon_type_icon = await apply_opacity(weapon_type_icon, 0.1)
        
        background.alpha_composite(weapon_type_icon,(666,369))
        
        
        items = await self.create_items()
        
        i = 0
        x = 688
        y = 277
        for key in items:
            if key["id"] == "2":
                background.alpha_composite(key["icon"], (687,96))
                continue
            
            background.alpha_composite(key["icon"], (x,y))
            x += 143
            i += 1
            
            if i == 4:
                x = 688
                y += 201
                
        effect_name= await create_image_with_text_v2(f"{self.data.effect_name}:", 52, 450, (255,255,255,255))
        desc_s1 = await create_image_with_text_v2(apply_params_to_effect(self.data.effect,  self.data.params, 0), 14, 545, (255,255,255,255))

        desc_s3 = await create_image_with_text_v2(apply_params_to_effect(self.data.effect,  self.data.params, 2), 14, 545, (255,255,255,255))
        desc_s5 = await create_image_with_text_v2(apply_params_to_effect(self.data.effect,  self.data.params, 4), 14, 545, (255,255,255,255))
        
        only_two = True
        
        if (effect_name.height*3) + desc_s1.height + desc_s3.height + desc_s5.height > 500:
            only_two = False
        
        y = 761
        draw = ImageDraw.Draw(background)
        font = await get_font(52)
        
        
        background.alpha_composite(effect_name, (735, y))
        draw.text((745+effect_name.width,y + effect_name.height-45), "S1", font = font, fill = (255,211,125,255))
        y += effect_name.height
        
        
        background.alpha_composite(desc_s1, (737, y))
        y += desc_s1.height +20
        
        if only_two:
            background.alpha_composite(effect_name, (735, y))
            draw.text((745+ effect_name.width,y+ effect_name.height-45), "S3", font = font, fill = (255,211,125,255))
            y += effect_name.height
        
            background.alpha_composite(desc_s3, (737, y))
            y += desc_s3.height +20
        
        background.alpha_composite(effect_name, (735, y))
        draw.text((745+effect_name.width,y+ effect_name.height-45), "S5", font = font, fill = (255,211,125,255))
        y += effect_name.height
        
        background.alpha_composite(desc_s5, (737, y))
        
        return background
    
    async def build(self, background_left, background_right):
        background:Image.Image = await files.background
        background = background.convert("RGBA").copy()

        background.alpha_composite(background_left)
        background.alpha_composite(background_right)
        
        return background
        
    async def start(self) -> Image.Image:
        files.set_mapping(5)
        
        background_left = await self.create_left_page()
        background_right = await self.create_right_page()
        
        return await self.build(background_left,background_right)
        
        
        
class WikiCharacterCard:
    def __init__(self, data: WikiCharacter, lang: str = "en"):
        self.data = data
        self.lang = lang
    
    async def create_character(self):
        self.character = Image.new("RGBA", (2639,1328), (0,0,0,0))
        icon = await get_download_img(self.data.icon.banner, (963,1328))
        icon_big = await get_download_img(self.data.icon.banner, (1287,1774))
        icon_big = await apply_opacity(icon_big, opacity= 0.1)
        self.character.alpha_composite(icon_big.convert("LA").convert("RGBA"),(578 ,-207))
        
        name = await create_image_with_text_v2(self.data.name.replace("-", " "), 339,1063, (255,255,255,12), padding_default = (3,25))
        self.character.alpha_composite(name,(475,230))
        name = await create_image_with_text_v2(self.data.name.replace("-", " "), 148,494, (255,212,122,255), padding_default = (80,25))
        self.character.alpha_composite(name,(580,305))
        self.character.alpha_composite(icon,(876,56))
        stars: Image.Image = await get_stars(self.data.rarity.id)
        
        self.character.alpha_composite(stars.resize((189,42)), (818, 305+name.height+10))


    async def create_constant(self):
        self.constant = Image.new("RGBA", (178,681), (0,0,0,0))
        frame_background = await files.character_constant
        
        position = [
            (0,0),
            (40,111),
            (66,223),
            (62,334),
            (36,455),
            (0,566),
        ]
        
        for i, key in enumerate(self.data.chains):
            background = Image.new("RGBA", (106,106), (0,0,0,0))
            icon = await get_download_img(self.data.chains.get(key).icon, size=(79,78))
            background.alpha_composite(frame_background)
            background.alpha_composite(icon, (15,15))
            self.constant.alpha_composite(background, position[i])
            
    
    async def create_skill(self):
        
        self.skill_background = Image.new("RGBA", (400,600), (0,0,0,0))
        font = await get_font(28)
        
        
        i_o = 0
        position_level_one = [
            (0,0),
            (137,0),
            (274,0),
        ]
        
        i_l = 0
        position_level = [
            (0,121),
            (137,121),
            (274,121),
            (0,242),
            (137,242),
            (0,363),
        ]
        
        for key in self.data.skill:
            info = self.data.skill.get(key).params
            
            icon = await get_download_img(info.icon, size=(85,83))
            
            background = await files.character_skill_frame
            background = background.copy()
            background.alpha_composite(icon,(29,21))
            
            icon_background = Image.new("RGBA", (150,151), (0,0,0,0))
            icon_background.alpha_composite(background)
            
            draw = ImageDraw.Draw(icon_background)
            x = int(font.getlength(f"MAX: {info.max_level}")/2)
            draw.text((75-x,125), f"MAX: {info.max_level}", font = font, fill = (255,211,125,255))

            if info.max_level == 1:
                self.skill_background.alpha_composite(icon_background.resize((121,121)),position_level_one[i_o])
                i_o += 1
            else:
                self.skill_background.alpha_composite(icon_background.resize((121,121)),position_level[i_l])
                i_l += 1
    
    async def skill_stats(self):
        self.skill_stats_background: Image.Image = await files.character_skill_stat
        items = []
        items_index = {}
        font = await get_font(28)
        position = [
                66,
                163,
                254,
                349
            ]
        
        for key in self.data.skill_trees:
            info = self.data.skill_trees.get(key).params
            icon = await get_download_img(info.icon, size=(50,50))
            if len(items) == 0:
                self.skill_stats_background.alpha_composite(icon, (3,14))
                items.append(info.name)
                items_index[info.name] = {"p": 0, "y": 28}
            elif len(items) == 1:
                self.skill_stats_background.alpha_composite(icon, (3,99))
                items.append(info.name)
                items_index[info.name] = {"p": 0, "y": 113}
            
            draw = ImageDraw.Draw(self.skill_stats_background)
            
            
            index = items_index[info.name]["p"]
            
            draw.text((position[index],items_index[info.name]["y"]), str(info.value_text[0]), font = font, fill = (255,255,255,255))
            items_index[info.name]["p"] += 1
            
                
    async def create_info_element_weapon(self):
        self.weapon_element = Image.new("RGBA", (517,259), (0,0,0,0))
        line = Image.new("RGBA", (517,5), (255,255,255,100))
        self.weapon_element.alpha_composite(line,(0,126))
        
        weapon_icon = await get_download_img(self.data.weapon.icon, size=(128,128))
        self.weapon_element.alpha_composite(weapon_icon)
        
        font = await get_font(52)
        draw = ImageDraw.Draw(self.weapon_element)
        draw.text((141,43), self.data.weapon.name, font = font, fill = (255,255,255,255))
        
        element_icon = await get_download_img(self.data.element.icon.get("3"), size=(128,128))
        self.weapon_element.alpha_composite(element_icon,(389,131))
        
        x = int(font.getlength(self.data.element.name))
        draw.text((376-x,171), self.data.element.name, font = font, fill = (255,255,255,255))
    
    async def create_items_icon(self, id: int, value: int):
        
        data = await utils.get_open_file(f"{self.lang}/items/{id}.json")
        
        if data == {}:
            data =  await utils.get_data(self.lang, catalog = "items", filename = str(id))
            
        background = Image.new("RGBA", (138,161), (0,0,0,0))
        frame = await get_frame_items(data.get("rarity").get("id"))
        icon = await get_download_img(data.get("icon").get("icon"), size=(112,112))
        background.alpha_composite(icon, (13,13))
        background.alpha_composite(frame)
        
        draw = ImageDraw.Draw(background)
        font = await get_font(22)
        x = int(font.getlength(str(value))/2)
        draw.text((69-x,141), str(value), font = font, fill = (255,255,255,255))
        
        
        return {"id": id, "icon": background}
    
    async def create_items(self):
        
        items_l = {}
        
        for key in self.data.ascensions:
            for items in self.data.ascensions[key]:
                if not items in items_l:
                    items_l[items] = self.data.ascensions[key][items]
                else:
                    items_l[items] += self.data.ascensions[key][items]

        icon = []
        items_l = utils.sort_items(items_l)
        for key in items_l:
            icon.append(await self.create_items_icon(key, items_l[key]))
        
        return icon
    
    async def create_ascension(self):
        items = await self.create_items()
        self.ascension_background = Image.new("RGBA", (868,339), (0,0,0,0))
        
        i = 0
        x = 146
        y = 0
        for key in items:
            if key["id"] == "2":
                self.ascension_background.alpha_composite(key["icon"], (0,0))
                continue
            
            self.ascension_background.alpha_composite(key["icon"], (x,y))
            x += 146
            i += 1
            
            if i == 5:
                x = 0
                y = 178
    
    async def create_stat(self):
        self.stat_background = await files.character_level_frame
        self.stat_background = self.stat_background.copy()
        
        position = [
            (189,70),
            (189,148),
            (189,224),
            (266,70),
            (266,148),
            (266,224),
        ]
        
        position_two = [
            (633,70),
            (633,148),
            (633,224),
            (711,70),
            (711,148),
            (711,224),
        ]
        
        draw = ImageDraw.Draw(self.stat_background)
        font = await get_font(46)
        
        for i, key in enumerate(self.data.stats):
            icon = await get_download_img(self.data.stats[key].icon, size=(62,62))
            if i > 2:
                self.stat_background.alpha_composite(icon, position[i])
                self.stat_background.alpha_composite(icon, position_two[i])
            else:
                self.stat_background.alpha_composite(icon, position[i])

            if self.data.stats[key].is_ration:
                value = f'{self.data.stats[key].value}%'
            else:
                value = str(self.data.stats[key].value)
                
            x = int(font.getlength(value))
            if i > 2:
                draw.text((position[i][0]+icon.width+7,position[i][1]+7), value, font = font, fill = (255,255,255,255))
                draw.text((position_two[i][0]+icon.width+7,position_two[i][1]+7), value, font = font, fill = (255,255,255,255))
            else:
                draw.text((position[i][0]-x-7,position[i][1]+7), value, font = font, fill = (255,255,255,255))
                
        position = [
            (-100,-100),
            (633,70),
            (633,148),
            (633,224),
            (711,70),
            (711,148),
            (711,224),
        ]
        
        for i, key in enumerate(self.data.stats_level["6"]["90"]):
            if key[0] == "level":
                continue
            icon = await get_download_img(key[1].icon, size=(62,62))
            self.stat_background.alpha_composite(icon, position[i])

            if key[1].is_ration:
                value = f'{key[1].value}%'
            else:
                value = str(round(key[1].value))
                
            x = int(font.getlength(value))
            if i > 3:
                draw.text((position[i][0]+icon.width+7,position[i][1]+7), value, font = font, fill = (255,255,255,255))
            else:
                draw.text((position[i][0]-x-7,position[i][1]+7), value, font = font, fill = (255,255,255,255))

    async def create_food(self):
        food:Image.Image = await files.character_food_background
        food = food.copy()
        if self.data.special_cook is None:
            self.food = Image.new("RGBA", (1,1), (0,0,0,0))
            return 
        
        icon = await get_download_img(self.data.special_cook.icon, size=(209,209))
        food.alpha_composite(icon,(72,6))
        
        
        name = await create_image_with_text_v2(self.data.special_cook.name, 46, 396, (255,212,122,255), padding_default = (20,5))
        description = await create_image_with_text_v2(self.data.special_cook.description, 21, 396, (255,255,255,255), padding_default = (20,5))
        
        height = name.height + description.height + 5 + 3
        if height < food.height:
            height = food.height
            
        self.food = Image.new("RGBA", (398+name.width + 10, height + 5 + 3), (0,0,0,0))
        
        self.food.alpha_composite(food)
        self.food.alpha_composite(name, (298,3))
        self.food.alpha_composite(description, (298, 8 + name.height))
          
    async def create_birthday(self):
        self.birthday = Image.new("RGBA", (768,50), (0,0,0,0))
        if self.data.info is None:
            return
        draw = ImageDraw.Draw(self.birthday)
        font = await get_font(47)
        x = int(font.getlength("BIRTHDAY:"))
        draw.text((0,0), "BIRTHDAY:", font = font, fill = (255,255,255,255))
        
        draw.text((3+x,0), self.data.info.birthday, font = font, fill = (255,212,122,255))
        
    async def create_desc(self):
        
        description_title = await create_image_with_text_v2("DESCRIPTION...", 64, 566, (255,212,122,255), padding_default = (20,5))
        description = await create_image_with_text_v2(self.data.description, 25, 842, (255,255,255,255))
        
        self.description = Image.new("RGBA", (description.width + 50,description_title.height + 20 + description.height), (0,0,0,0))
        self.description.alpha_composite(description_title)
        self.description.alpha_composite(description, (0, description_title.height + 10))
        
    
    async def build(self):
        background: Image.Image = await files.character_background
        line = await files.character_line
        character_ascension_line = await files.character_ascension_line
        background = background.convert("RGBA").copy()
        background.alpha_composite(self.character)
        background.alpha_composite(self.constant, (1582,513))
        background.alpha_composite(self.skill_background,(9,100))
        background.alpha_composite(self.skill_stats_background,(9,529))   
        background.alpha_composite(self.weapon_element,(470,555))
        background.alpha_composite(self.ascension_background,(16,926))
        background.alpha_composite(self.stat_background,(1732,143))
        background.alpha_composite(self.food,(1732,488))
        background.alpha_composite(self.birthday,(1790,808))
        background.alpha_composite(self.description,(1790,910))
        background.alpha_composite(line, (752,1289))
        background.alpha_composite(character_ascension_line, (160,1081))
        
        return background
        
        
    async def start(self) -> Image.Image:
        files.set_mapping(5)
        
        await self.create_character()
        await self.create_info_element_weapon()
        await self.create_constant()
        await self.create_skill()
        await self.skill_stats()
        await self.create_ascension()
        await self.create_stat()
        await self.create_food()
        await self.create_birthday()
        await self.create_desc()
        
        return await self.build()