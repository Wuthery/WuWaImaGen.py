from .src.components import convene, event, business_card, material


class ClientWuWa(event.EventClient,
                 convene.ConveneClient,
                 business_card.BusinessCardClient,
                 material.CalculatorMaterial):
    pass

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        pass

        
    