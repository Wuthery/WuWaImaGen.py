import asyncio
import wuwaimagen

'''
This example allows you to generate a gacha card and calculate your luck.
More examples here: https://github.com/Wuthery/WuWaImaGen.py/tree/main/Example
'''

client = wuwaimagen.ClientWuWa(assets=True)

config = {
    "resonator": [1402,"1503", 1404],
    "uid": 600329448,
    "resonator_art": {
        "1402": "https://i.pximg.net/img-master/img/2024/06/17/13/03/36/119719985_p0_master1200.jpg",
        "1503":"https://i.pximg.net/img-master/img/2024/05/27/18/09/36/119100858_p0_master1200.jpg"
    },
    "nickname": "Korzzex",
    "screenshot": "https://dotesports.com/wp-content/uploads/2024/05/WuWa.jpg"
}


async def main():    
    async with client:
        data = await client.get_card(
            level = 81,
            signature= "Did you think I was a programmer?",
            config= config
        )
        
        data.save("BusinessCardExample.png")

                
asyncio.run(main())
