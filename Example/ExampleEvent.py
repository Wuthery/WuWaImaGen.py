import asyncio
import wuwaimagen

'''
This example allows you to get events in the game and generate a calendar card
More examples here: https://github.com/Wuthery/WuWaImaGen.py/tree/main/Example
'''

client = wuwaimagen.ClientWuWa(assets = True)

async def main():
    async with client:
        data = await client.get_event_info(generator=True)
        print(data)

asyncio.run(main())
