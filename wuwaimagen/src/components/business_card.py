from PIL import Image
from random import choice
from typing import Union, Dict, Sequence
from .main import MainWuWaImaGen
from ..model.business_card import Config
from ..tools import git
from ..generator.business_card import CardConvene



_PLAY_STYLE = [
    "Free to play",
    "I Love Seria",
    "JokelBaf.Enum",
    "Ashlen - You Name?",
    "goatchita just goatchita"
    "Save programming daemon",
    "Anubhav RGBA PLS!!!"
    "Дайте пива Korzzex!!!"
    
]

class BusinessCardClient(MainWuWaImaGen):
    
    
    def check_params(self):
        if not isinstance(self.resonator, list):
            raise TypeError("The resonator argument must be a list containing str or int values ​​of the Resonator ID")
        else:
            if self.resonator == []:
                self.resonator = self.config.get("resonator", [])
            for key in self.resonator:
                if not isinstance(key, (str,int)):
                    self.resonator.remove(key)
                    
        if self.resonator_art is None:
            self.resonator_art = self.config.get("resonator_art", None)
        if not self.resonator_art is None:   
            if not isinstance(self.resonator_art, dict):
                raise TypeError("The resonator_art argument must be a dictionary where the key resonator id is a string or number and the value is a string")
            else:
                for key in self.resonator_art:
                    if not isinstance(self.resonator_art[key], str):
                        del self.resonator_art[key]
        
        if self.uid is None:
            self.uid = self.config.get("uid", 0)
            
        if not isinstance(self.uid, (str,int)):
            raise TypeError("The uid argument must be a number or a string")
        
        if self.level < 1:
            self.level = 1
        
        if self.level > 80:
            self.level = 80
            
        params = {
            'resonator': self.resonator,
            'uid': self.uid,
            'resonator_art': self.resonator_art,
            'nickname': self.nickname,
            "play_style": self.play_style[:24],
            'level':self.level,
            'screenshot': self.screenshot,
            'signature': self.signature,
        }
        
        for key, value in params.items():
            if not key in self.config:
                self.config[key] = value
        
        self.config = Config(**self.config) 
    

    async def get_business_card(
        self, 
        resonator: Sequence[Union[str,int]] = [], 
        uid: Union[str,int] = None,
        resonator_art: Dict[Union[str,int], str] = None,
        nickname: str = "User Name",
        play_style: str = choice(_PLAY_STYLE),
        level: Union[str,int] = 1,
        screenshot: str = None,
        signature: str = None,
        config: Dict[str, Union[list,dict,str]] = {}
        ) -> Image.Image:
        
        
        self.resonator = resonator
        self.uid = uid
        self.resonator_art = resonator_art
        self.nickname = nickname
        self.play_style = play_style
        self.level = level
        self.screenshot = screenshot
        self.signature = signature
        self.config = config
        
        self.check_params()      
          
        await git.ImageCache.set_assets_download(self.assets)
        
        return await CardConvene(self.config).start()
        
    
    
        