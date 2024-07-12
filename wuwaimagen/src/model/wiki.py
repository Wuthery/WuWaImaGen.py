from typing import List, Optional, Sequence, Union, Mapping
from pydantic import BaseModel, Field
from PIL import Image



class WikiType(BaseModel):
    id: int
    name: str
    icon: str

class RarityWeapon(BaseModel):
    id: int
    name: str
    color: str

class IconWeapon(BaseModel):
    icon: str
    icon_middle: str
    icon_small: str

class StatsWeaponInfo(BaseModel):
    attribute: str
    name: str
    value: Union[int,float]
    is_ration: bool
    icon: str
   
class WikiWeapon(BaseModel):
    id: int
    name: str
    type: WikiType
    rarity: RarityWeapon
    description: str
    icon: IconWeapon
    effect: str
    effect_name: str
    params: Mapping[str, List]
    stats: Mapping[str, StatsWeaponInfo]
    stats_level: Mapping[str, Mapping[str,List[StatsWeaponInfo]]]
    ascensions: Mapping[str, Mapping[str, Union[int,float]]]
    card: Optional[Image.Image] = Field(None)

    class Config:
        arbitrary_types_allowed = True
        

class RarityCharacter(BaseModel):
    id: int
    name: str
    consume_text: str
    color: str
    stars: str
    
class ElementCharacter(BaseModel):
    id: int
    name: str
    description: str
    color: str
    icon: Mapping[str,str]

class IconCharacter(BaseModel):
    icon: Optional[str]
    icon_round: Optional[str]
    banner: Optional[str]    

class ConstantCharacter(BaseModel):
    id: int
    value: int
    icon: str
    name: str
    description: str
    rarity: RarityCharacter

class InfoCharacter(BaseModel):
    birthday: str
    country: str
    influence: str
    sex: str
    talent_certification: str
    talent_doc: str
    talent_name: str
    cv_name: Mapping[str,str]
    
class StoriesCharacter(BaseModel):
    id: int
    title: str
    content: str

class VoiceCharacter(BaseModel):
    id: int
    sort: int
    title: str
    content: str

class GoodsCharacter(BaseModel):
    id: int
    sort: int
    title: str
    content: str
    icon: str

class Cook(BaseModel):
    id: int
    recept_id: int
    name: str
    rarity: RarityCharacter
    description: str
    icon: str

class CharacterStats(BaseModel):
    key: str
    name: str
    value: Union[int, float]
    is_ration: bool
    icon: str
    
class CharacterStatsLevel(BaseModel):
    level: int
    life: CharacterStats
    atk: CharacterStats
    def_: CharacterStats = Field(alias="def")


class CharterChains(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    param: list

class SkillTreesValue(BaseModel):
    id: int = Field(alias="Id")
    value: Union[int, float] = Field(alias="Value")
    is_ratio: int = Field(alias="IsRatio")

class SkillTreesParams(BaseModel):
    name: str
    description: str
    value: List[SkillTreesValue]
    value_text: list
    icon: str
    max_level: int
    
class SkillTrees(BaseModel):
    id: int
    consume: Mapping[str,int]
    coordinate: int
    params:SkillTreesParams
    type: int
    parent_nodes: list
    unLock: int
    tree: bool

class SkillLevel(BaseModel):
    id: int
    name: str
    params: list
    

class SkillParams(BaseModel):
    name: str
    description: str
    level: Mapping[str,SkillLevel]
    icon: str
    max_level: int

class Skill(BaseModel):
    id: int
    consume: Mapping[str,int]
    params: SkillParams
    type: int
    sort: int
    unLock: int
    tree: bool
    
        
class WikiCharacter(BaseModel):
    id: int
    name: str
    nickname: str
    weapon: WikiType
    rarity: RarityCharacter
    element: ElementCharacter
    description: str
    icon: IconCharacter
    constant: ConstantCharacter
    info: Optional[InfoCharacter]
    stories: Mapping[str, StoriesCharacter]
    voice: Mapping[str, VoiceCharacter]
    goods: Mapping[str, GoodsCharacter]
    special_cook: Optional[Cook]
    stats: Mapping[str, CharacterStats]
    stats_level: Mapping[str, Mapping[str,CharacterStatsLevel]]
    chains: Mapping[str, CharterChains]
    skill_trees: Mapping[str, SkillTrees]
    skill:Mapping[str, Skill]
    ascensions: Mapping[str, Mapping[str, Union[int,float]]]
    card: Optional[Image.Image] = Field(None)

    class Config:
        arbitrary_types_allowed = True
    