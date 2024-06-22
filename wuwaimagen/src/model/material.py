# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Optional, Mapping, List
from PIL import Image

class StatBonusAttackLevel(IntEnum):
    """
    An enumeration representing the attack level bonus.
    
    Attributes:
    - off (int): Disable all.
    - minimal (int): Include only the first.
    - maximal (int): Include only the second.
    - full (int): Enable all.
    
    """
    off = 0
    minimal = 1
    maximal = 2
    full = 3

class StatBonusResonatorSkill(IntEnum):
    """
    An enumeration representing the resonator skill bonus.
    
    Attributes:
    - off (int): Disable all.
    - minimal (int): Include only the first.
    - maximal (int): Include only the second.
    - full (int): Enable all.
    
    """
    off = 0
    minimal = 1
    maximal = 2
    full = 3

class StatBonusResonanceLiberation(IntEnum):
    """
    An enumeration representing the resonance liberation bonus.
    
    Attributes:
    - off (int): Disable all.
    - minimal (int): Include only the first.
    - maximal (int): Include only the second.
    - full (int): Enable all.
    
    """
    off = 0
    minimal = 1
    maximal = 2
    full = 3

class StatBonusIntroSkill(IntEnum):
    """
    An enumeration representing the introduction skill bonus.
    
    Attributes:
    - off (int): Disable all.
    - minimal (int): Include only the first.
    - maximal (int): Include only the second.
    - full (int): Enable all.
    
    """
    off = 0
    minimal = 1
    maximal = 2
    full = 3

class StatBonusForteCircuit(IntEnum):
    """
    An enumeration representing the forte circuit bonus.
    
    Attributes:
    - off (int): Disable all.
    - minimal (int): Include only the first.
    - maximal (int): Include only the second.
    - full (int): Enable all.
    
    """
    off = 0
    minimal = 1
    maximal = 2
    full = 3

class Level(BaseModel):
    """
    A model representing a level with minimum and maximum values.

    Attributes:
    - min (int): Minimum level value.
    - max (int): Maximum level value.
    """
    min: int = Field(1, ge=1)
    max: int = Field(10, ge=1, le=90)

class StatBonus(BaseModel):
    """
    A model representing various stat bonuses.

    Attributes:
    - attack_level (StatBonusAttackLevel): The attack level bonus.
    - resonator_skill (StatBonusResonatorSkill): The resonator skill bonus.
    - resonance_liberation (StatBonusResonanceLiberation): The resonance liberation bonus.
    - intro_skill (StatBonusIntroSkill): The introduction skill bonus.
    - forte_circuit (StatBonusForteCircuit): The forte circuit bonus.
    """
    attack_level: StatBonusAttackLevel = Field(StatBonusAttackLevel.full)
    resonator_skill: StatBonusResonatorSkill = Field(StatBonusResonatorSkill.full)
    resonance_liberation: StatBonusResonanceLiberation = Field(StatBonusResonanceLiberation.full)
    intro_skill: StatBonusIntroSkill = Field(StatBonusIntroSkill.full)
    forte_circuit: StatBonusForteCircuit = Field(StatBonusForteCircuit.full)
    
    @property
    def list(self) -> List[IntEnum]:
        """
        Returns a list of all stat bonuses.
        """
        return [
            self.attack_level,
            self.resonator_skill,
            self.resonance_liberation,
            self.intro_skill,
            self.forte_circuit,
        ]

class MaterialCharacter(BaseModel):
    """
    A model representing a character with various attributes and levels.

    Attributes:
    - id (int): The character ID.
    - level (Level): The character's overall level.
    - normal_attack (Level): The normal attack level.
    - resonator_skill (Level): The resonator skill level.
    - resonance_liberation (Level): The resonance liberation level.
    - intro_skill (Level): The introduction skill level.
    - forte_circuit (Level): The forte circuit level.
    - stat_bonus (StatBonus): The stat bonuses.
    """
    id: int = Field(None, ge=1000, le=9999)
    level: Level = Field(default_factory=lambda: Level(min=1, max=90))
    normal_attack: Level = Field(default_factory=lambda: Level(min=1, max=10))
    resonator_skill: Level = Field(default_factory=lambda: Level(min=1, max=10))
    resonance_liberation: Level = Field(default_factory=lambda: Level(min=1, max=10))
    intro_skill: Level = Field(default_factory=lambda: Level(min=1, max=10))
    forte_circuit: Level = Field(default_factory=lambda: Level(min=1, max=10))
    stat_bonus: StatBonus = Field(StatBonus())

class MaterialWeapon(BaseModel):
    """
    A model representing a weapon with various attributes and levels.

    Attributes:
    - id (int): The weapon ID.
    - level (Level): The weapon's level.
    """
    id: int = Field(None, ge=10000)
    level: Level = Field(Level(min=1, max=90))

class Material(BaseModel):
    """
    A model representing a material with various attributes.

    Attributes:
    - id (int): The material ID.
    - icon (str): The material icon.
    - rarity (int): The material rarity.
    - value (int): The material value.
    """
    id: int
    icon: str
    rarity: int
    value: int

class WeaponInfo(BaseModel):
    """
    A model representing weapon information.

    Attributes:
    - id (int): The weapon ID.
    - name (str): The weapon name.
    - rarity (int): The weapon rarity.
    - icon (str): The weapon icon.
    """
    id: int
    name: str
    rarity: int
    icon: str

class CharacterInfo(BaseModel):
    """
    A model representing character information.

    Attributes:
    - id (int): The character ID.
    - name (str): The character name.
    - element_id (int): The element ID associated with the character.
    - banner (str): The character banner.
    - rarity (int): The character rarity.
    """
    id: int
    name: str
    element_id: int
    banner: str
    rarity: int

class CalculatorMaterialModel(BaseModel):
    """
    A model representing a calculator for materials with character, weapon, and other information.

    Attributes:
    - items (Mapping[int, Material]): A mapping of material IDs to Material objects.
    - character (CharacterInfo): Information about a character.
    - weapon (WeaponInfo): Information about a weapon.
    - card (Optional[Image.Image]): An optional image card.
    """
    items: Mapping[int, Material]
    character: CharacterInfo = Field(None)
    weapon: WeaponInfo = Field(None)
    card: Optional[Image.Image] = Field(None)

    class Config:
        arbitrary_types_allowed = True
