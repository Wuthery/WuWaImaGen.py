import time
from ..tools.utils import get_event_list
from ..model.event import EvenList
from ..generator.event import CardEvent
from .main import MainWuWaImaGen
from ..tools import git

class EventClient(MainWuWaImaGen):

    async def get_event_info(self, generator: bool = False) -> EvenList:
        """Generates a picture calendar with events
        
        Args:
            generator (bool, optional): Generate a card or not. Defaults to False.
        
        Returns:
            EvenList: BaseModel
        """
        await git.ImageCache.set_assets_download(self.assets)
        
        payload = {
            "time": int(time.time()),
            "type": "list"
        }
        
        event_data = EvenList(**await get_event_list(payload))
        
        if generator: 
            
            event_data.card = await CardEvent(event_data.activity).start()
        
        return event_data
        