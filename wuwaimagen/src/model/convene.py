# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import datetime
from PIL import Image
from typing import List, Optional
from pydantic import BaseModel, Field
from ..settings.other import WUTHERY_CDN


class RecordIcon(BaseModel):
    icon: str
    banner: str
    
class SpinInfo(BaseModel):
    resonator: int
    weapon: int

class Next(BaseModel):
    five: int
    four: int

class Info(BaseModel):
    total_spin: int
    astrite: int
    next: Next
    five_stars: SpinInfo
    four_stars: SpinInfo
    three_stars: SpinInfo

class Color(BaseModel):
    hex: str
    rgba: tuple

class RecordCalculator(BaseModel):
    typeRecord: Optional[int] = Field(1)
    cardPoolType: str
    resourceId: int
    qualityLevel: int
    resourceType: str
    name: str
    count: int
    time: datetime.datetime
    drop: int
    color: Color
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(str(self.resourceId)) > 5:
            self.typeRecord = 2       
    
    async def get_icon(self):
        if len(str(self.resourceId)) > 5:
            icon = WUTHERY_CDN +  f"d/GameData/UIResources/Common/Image/IconWeapon/T_IconWeapon{self.resourceId}_UI.png"
            return RecordIcon(icon = icon, banner = icon)
        else:
            ''' ===== Outdated way =======
            data = await get_data_resonator(self.resourceId)
            if data is None:
                return None
            icon = data.get("Icon", "").split(".")[1]
            banner = data.get("Background", "").split(".")[1]
            '''
            
            return RecordIcon(icon = WUTHERY_CDN + f"d/GameData/IDFiedResources/Common/Image/IconRoleHead256/{self.resourceId}.png", banner = WUTHERY_CDN + f"d/GameData/IDFiedResources/Common/Image/IconRolePile/{self.resourceId}.png")

class Calculator(BaseModel):
    info: Info
    data: List[RecordCalculator]
    gacha_id: Optional[int] = Field(1)
    card: Optional[Image.Image] = Field(None)
    
    class Config:
        arbitrary_types_allowed = True