# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from __future__ import annotations

from typing import List, Optional
from PIL import Image
from pydantic import BaseModel, Field
from datetime import datetime

class GameDatetime(BaseModel):
    start: datetime
    end: datetime

class TabTitle(BaseModel):
    zh_Hans: str = Field(..., alias='zh-Hans')
    zh_Hant: str = Field(..., alias='zh-Hant')
    en: str
    ja: str
    ko: str
    fr: str
    de: str
    es: str


class TabBanner(BaseModel):
    zh_Hans: List[str] = Field(..., alias='zh-Hans')
    zh_Hant: List[str] = Field(..., alias='zh-Hant')
    en: List[str]
    ja: List[str]
    ko: List[str]
    fr: List[str]
    de: List[str]
    es: List[str]


class GameItem(BaseModel):
    contentPrefix: List[str]
    red: int
    permanent: int
    id: str
    startTimeMs: int
    endTimeMs: int
    platform: List[int]
    channel: List
    whiteList: List
    tabTitle: TabTitle
    tabBanner: TabBanner
    
    def time(self):
        return GameDatetime(start = datetime.fromtimestamp(self.startTimeMs / 1000), end = datetime.fromtimestamp(self.endTimeMs / 1000))

class ActivityItem(BaseModel):
    contentPrefix: List[str]
    red: int
    permanent: int
    id: str
    startTimeMs: int
    endTimeMs: int
    platform: List[int]
    channel: List
    whiteList: List
    tabTitle: TabTitle
    tabBanner: TabBanner

    def time(self):
        return GameDatetime(start = datetime.fromtimestamp(self.startTimeMs / 1000), end = datetime.fromtimestamp(self.endTimeMs / 1000))

class EvenList(BaseModel):
    game: List[GameItem]
    activity: List[ActivityItem]
    card: Optional[Image.Image] = Field(None)

    class Config:
        arbitrary_types_allowed = True