import abc



class MainWuWaImaGen(abc.ABC):
    
    def __init__(self, assets: bool = False) -> None:
        """Main class

        Args:
            assets (bool, optional): Save assets to device, fills device storage. Defaults to False.
        """
        self.assets = assets
        super().__init__()
        