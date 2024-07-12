from typing import Union
from .main import MainWuWaImaGen
from ..model.material import CharacterInfo, MaterialCharacter, MaterialWeapon, CalculatorMaterialModel, Level, WeaponInfo
from ..tools import git, utils
from ..generator.material_character import CardCharacterMaterial
from ..generator.material_weapon import CardWeaponMaterial


class CalculatorMaterial(MainWuWaImaGen):
    
    async def loading_material(self):
        self.ItemInfo = await utils.get_open_file("ItemInfo")
        self.RoleInfo = await utils.get_open_file("RoleInfo")
        self.WeaponBreach = await utils.get_open_file("WeaponBreach")
        self.WeaponConf = await utils.get_open_file("WeaponConf")
        self.SkillTree = await utils.get_open_file("SkillTree")
        self.SkillLevel = await utils.get_open_file("SkillLevel")
        self.RoleBreach =  await utils.get_open_file("RoleBreach")
        self.MultiText  = await utils.get_open_file("en/MultiText")
    
    async def update_json_file(self):
        self.ItemInfo = await utils.get_data_resonator("ItemInfo")
        self.RoleInfo = await utils.get_data_resonator("RoleInfo")
        self.WeaponBreach = await utils.get_data_resonator("WeaponBreach")
        self.WeaponConf = await utils.get_data_resonator("WeaponConf")
        self.SkillTree = await utils.get_data_resonator("SkillTree")
        self.SkillLevel = await utils.get_data_resonator("SkillLevel")
        self.RoleBreach =  await utils.get_data_resonator("RoleBreach")
        self.MultiText  = await utils.get_textMap(lang= self.lang, filename = "MultiText")

    
    async def get_items(self):
        items = {}

        for key in self.consume:
            item = next(filter(lambda x: x["Id"] == int(key), self.ItemInfo), None)
            if not item  is None:
                icon = item.get("Icon").split("Image")[1].split(".")[0]
                items[key] = {"id": int(key), "icon": utils.link_icon + icon + ".png", "rarity": item.get("QualityId"), "value": self.consume[key]}

        return utils.sort_items(items)
    
    async def add_role_breach(
        self,
        resonator_level: Level
        ):
        breach_level_min = utils.get_breach_level(resonator_level.min)
        breach_level_max = utils.get_breach_level(resonator_level.max)
        
        
        for key in self.RoleBreach:
            if key["BreachGroupId"] == self.role_info_id:
                if key["BreachLevel"] > breach_level_min and key["BreachLevel"] <= breach_level_max:
                    for items_id in key["BreachConsume"]:
                        if not items_id in self.consume:
                            self.consume[items_id] = key["BreachConsume"][items_id]
                        else:
                            self.consume[items_id] += key["BreachConsume"][items_id]
                '''
                else:
                    for items_id in key["BreachConsume"]:
                        if not items_id in self.consume:
                            self.consume[items_id] = 0
                        else:
                            self.consume[items_id] += 0
                '''
        
    async def get_skill_add_skill_tree(self):
        skill_id = []
        
        for key in self.SkillTree:
            if key.get("NodeGroup", 0) == self.role_info_id:
                if key["SkillId"] != 0:
                    skill_id.append(key["SkillId"])
                    continue
                
                parent_nodes = key["Id"]
                if utils.status_stat_bonus(parent_nodes, self.stat_bonus.list):
                    for items_id in key["Consume"]:
                        if not items_id in self.consume:
                            self.consume[items_id] = key["Consume"][items_id]
                        else:
                            self.consume[items_id] += key["Consume"][items_id]
        return skill_id
    
    async def add_skill(
        self,
        skill_id:list,
        normal_attack: Level,
        resonator_skill: Level,
        resonance_liberation: Level,
        intro_skill: Level,
        forte_circuit: Level,
        ):
        for key in self.SkillLevel:
            if key["SkillLevelGroupId"] in skill_id:
                
                parent_nodes = str(key["SkillLevelGroupId"])[-1:]
                
                if not utils.status_stat_bonus(int(parent_nodes), self.stat_bonus.list):
                    continue
                
                if str(key["SkillLevelGroupId"])[-1:] == "1":
                    if normal_attack.min>= key["SkillId"] or normal_attack.max < key["SkillId"]:
                        continue

                if str(key["SkillLevelGroupId"])[-1:] == "2":
                    if resonator_skill.min >= key["SkillId"] or resonator_skill.max < key["SkillId"]:
                        continue

                if str(key["SkillLevelGroupId"])[-1:] == "3":
                    if resonance_liberation.min >= key["SkillId"] or resonance_liberation.max < key["SkillId"]:
                        continue

                if str(key["SkillLevelGroupId"])[-1:] == "6":
                    if intro_skill.min >= key["SkillId"] or intro_skill.max < key["SkillId"]:
                        continue

                if str(key["SkillLevelGroupId"])[-1:] == "7":
                    if forte_circuit.min >= key["SkillId"] or forte_circuit.max < key["SkillId"]:
                        continue
                
                if key["Consume"] is None:
                    continue
                
                for items_id in key["Consume"]:
                    if not items_id in self.consume:
                        self.consume[items_id] = key["Consume"][items_id]
                    else:
                        self.consume[items_id] += key["Consume"][items_id]
    
    async def get_character(self, config: MaterialCharacter) -> CharacterInfo:
        role_info_data: dict = next(filter(lambda x: x["Id"] == int(config.id), self.RoleInfo), None)
            
        if role_info_data is None:
            await self.update_json_file()
            role_info_data: dict = next(filter(lambda x: x["Id"] == int(config.id), self.RoleInfo), None)
        
        if role_info_data is None:
            raise TypeError("This ID was not found, check the id values")
        
        self.role_info_id = role_info_data.get("SkillTreeGroupId")
        self.stat_bonus = config.stat_bonus

        await self.add_role_breach(config.level)
        
        skill_id = await self.get_skill_add_skill_tree()

        await self.add_skill(
            skill_id,
            config.normal_attack,
            config.resonator_skill,
            config.resonance_liberation,
            config.intro_skill,
            config.forte_circuit
            )

        character = CharacterInfo(
            id = self.role_info_id,
            name = self.MultiText.get(role_info_data.get("Name"), "Name"),
            element_id =  role_info_data.get("ElementId", 1),
            rarity = role_info_data.get("QualityId", 4),
            banner = utils.WUTHERY_CDN + f"p/GameData/IDFiedResources/Common/Image/IconRolePile/{self.role_info_id}.png"
        )
        
        return character
    
    async def get_items_weapon(self, id: int, weapon_level: Level):
        if self.WeaponBreach == {}:
            await self.update_json_file()

        breach_level_max = utils.get_breach_level(weapon_level.max) - 1
        ""
        
        for key in self.WeaponBreach:
            if key["BreachId"] == id:
                if key["Level"] <= breach_level_max:
                    if not "2" in self.consume:
                        self.consume["2"] = key["GoldConsume"]
                    else:
                        self.consume["2"] += key["GoldConsume"]
                    
                    for items in key["Consume"]:
                        if not items in self.consume:
                            self.consume[items] = key["Consume"][items]
                        else:
                            self.consume[items] += key["Consume"][items]
               
    async def get_weapon(self, config: MaterialWeapon) -> WeaponInfo:
        weapon_id: dict = next(filter(lambda x: x["BreachId"] == int(config.id), self.WeaponBreach), None)
            
        if weapon_id is None:
            await self.update_json_file()
            weapon_id: dict = next(filter(lambda x: x["BreachId"] == int(config.id), self.WeaponBreach), None)
        
        if weapon_id is None:
            raise TypeError("This ID was not found, check the id values")
        
        await self.get_items_weapon(weapon_id.get("BreachId"), config.level)
                
        weapon_info = next(filter(lambda x: x["ItemId"] == int(config.id), self.WeaponConf), None)
        name = weapon_info.get("WeaponName")
        
        return  WeaponInfo(id = weapon_info.get("ItemId"), name = self.MultiText.get(name), rarity= weapon_info.get("QualityId"), icon=  utils.WUTHERY_CDN +  f"p/GameData/UIResources/Common/Image/IconWeapon/T_IconWeapon{weapon_info.get("ItemId")}_UI.png")
    
    async def get_material(
        self, 
        config: Union[MaterialCharacter,MaterialWeapon],
        card: bool = False
        ) -> CalculatorMaterialModel:

        
        await git.ImageCache.set_assets_download(self.assets)
        
        await self.loading_material()
        
        self.consume = {}
        
        if config.__class__ == MaterialWeapon:
            weapon = await self.get_weapon(config)
            result = await self.get_items()
                        
            result = CalculatorMaterialModel(items = result, weapon =  weapon, card = None)
            
            if card:
                result.card = await CardWeaponMaterial(result).start(config.level)
            
        else:            
            character = await self.get_character(config)
            result = await self.get_items()
            result = CalculatorMaterialModel(items = result, character = character, card = None)
            if card:
                result.card = await CardCharacterMaterial(result).start(config.level)
        
        return result
    