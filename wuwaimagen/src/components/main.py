import abc



class MainWuWaImaGen(abc.ABC):
    
    def __init__(self, lang:str = "en", assets: bool = False) -> None:
        """Main class

        Args:
            lang (str, optional): Set the language for the module
            assets (bool, optional): Save assets to device, fills device storage. Defaults to False.
        """
        self.lang: str = lang
        self.assets: bool = assets
        super().__init__()
    
    def set_lang(self, lang: str = "en"):
        self.lang = lang