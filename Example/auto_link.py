import asyncio

import wuwaconvene


async def main():
    link = await wuwaconvene.auto_link(r"D:\Wuthering Waves")
    print(link)


asyncio.run(main())
