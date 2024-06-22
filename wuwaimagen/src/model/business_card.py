from typing import List, Optional, Sequence, Union, Mapping
from pydantic import BaseModel, Field


class Config(BaseModel):
    resonator: Sequence[Union[str,int]]
    uid: Union[str,int]
    resonator_art: Optional[Mapping[Union[str,int], str]] = Field(None)
    nickname: str
    play_style: str
    level: int
    screenshot: Optional[str] = Field(None)
    signature: Optional[str] = Field(None)