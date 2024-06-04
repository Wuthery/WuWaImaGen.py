import datetime
from PIL import Image
from typing import List, Optional
from pydantic import BaseModel, Field
from .uttils import get_data_resonator

class RecordIcon(BaseModel):
    icon: str
    banner: str
    

class Record(BaseModel):
    typeRecord: Optional[int] = Field(1)
    cardPoolType: str
    resourceId: int
    qualityLevel: int
    resourceType: str
    name: str
    count: int
    time: datetime.datetime
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(str(self.resourceId)) > 5:
            self.typeRecord = 2       
    
    async def get_icon(self):
        if len(str(self.resourceId)) > 5:
            icon = f"https://api.hakush.in/ww/UI/UIResources/Common/Image/IconWeapon/T_IconWeapon{self.resourceId}_UI.webp"
            return RecordIcon(icon = icon, banner = icon)
        else:
            data = await get_data_resonator(self.resourceId)
            if data is None:
                return None
            icon = data.get("Icon", "").split(".")[1]
            banner = data.get("Background", "").split(".")[1]
            
            return RecordIcon(icon = f"https://api.hakush.in/ww/UI/UIResources/Common/Image/IconRoleHead256/{icon}.webp", banner = f"https://api.hakush.in/ww/UI/UIResources/Common/Image/IconRolePile/{banner}.webp")

class ConveneData(BaseModel):
    code: int
    message: str
    data: Optional[List[Record]]
    gacha_id: Optional[int] = Field(1)


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
            icon = f"https://api.hakush.in/ww/UI/UIResources/Common/Image/IconWeapon/T_IconWeapon{self.resourceId}_UI.webp"
            return RecordIcon(icon = icon, banner = icon)
        else:
            data = await get_data_resonator(self.resourceId)
            if data is None:
                return None
            icon = data.get("Icon", "").split(".")[1]
            banner = data.get("Background", "").split(".")[1]
            
            return RecordIcon(icon = f"https://api.hakush.in/ww/UI/UIResources/Common/Image/IconRoleHead256/{icon}.webp", banner = f"https://api.hakush.in/ww/UI/UIResources/Common/Image/IconRolePile/{banner}.webp")

class Calculator(BaseModel):
    info: Info
    data: List[RecordCalculator]
    gacha_id: Optional[int] = Field(1)
    card: Optional[Image.Image] = Field(None)
    
    class Config:
        arbitrary_types_allowed = True