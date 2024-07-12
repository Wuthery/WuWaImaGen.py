from .src.components import convene, event, business_card, material, wiki


class ClientWuWa(event.EventClient,
                 convene.ConveneClient,
                 business_card.BusinessCardClient,
                 material.CalculatorMaterial,
                 wiki.WikiInfo
                 ):
    pass

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        pass

        
    