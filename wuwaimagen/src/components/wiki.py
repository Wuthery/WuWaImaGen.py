from typing import Union
from .main import MainWuWaImaGen
from ..model.wiki import WikiWeapon, WikiCharacter
from ..tools import git, utils
from ..generator.wiki import WikiWeaponCard, WikiCharacterCard


class WikiInfo(MainWuWaImaGen):

    async def loading_info(self, type: int = 0):        
        if type == 0:
            self.data = await utils.get_open_file(f"grouped/{self.lang}/character/{self.id}.json")
        else:
            self.data = await utils.get_open_file(f"grouped/{self.lang}/weapon/{self.id}.json")

    async def update_json_file_wiki(self, catalog: str = "character"):
        self.data = await utils.get_data(self.lang, catalog = catalog, filename = str(self.id))
        
    async def get_wiki(self, id: int) -> WikiWeapon:
        
        self.id = id
        await git.ImageCache.set_assets_download(self.assets)
        
        if len(str(id)) > 5:
            await self.loading_info(1)
            if self.data == {}:
                await self.update_json_file_wiki(catalog="weapon")
                                
            data = WikiWeapon(**self.data)
            
            data.card = await WikiWeaponCard(data, self.lang).start()
        else:
            
            await self.loading_info()
            if self.data == {}:
                await self.update_json_file_wiki()

            data = WikiCharacter(**self.data)
            
                
            if data.id < 9000:
                data.card = await WikiCharacterCard(data, self.lang).start()

        return data