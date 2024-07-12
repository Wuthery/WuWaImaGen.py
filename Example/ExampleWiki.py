import asyncio
import wuwaimagen

'''
This example allows you to get events in the game and generate a calendar card
More examples here: https://github.com/Wuthery/WuWaImaGen.py/tree/main/Example
'''

client = wuwaimagen.ClientWuWa(assets=True, lang = "en")

async def main():
    async with client:
        data = await client.get_wiki(1105)
        print(data)

asyncio.run(main())
