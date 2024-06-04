import asyncio

import WuWaConvene


async def main():
    async with WuWaConvene.Convene(
        link="https://aki-gm-resources-oversea.aki-game.net/aki/gacha/index.html#/record?svr_id=6eb2a235b30d05efd77bedb5cf60999e&player_id=600329448&lang=en&gacha_id=4&gacha_type=6&svr_area=global&record_id=97bfb175262ffb96a20874040b8662be&resources_id=917dfa695d6c6634ee4e972bb9168f6a"
    ) as convenes:
        data = await convenes.get(7, lang="en", generator=True)
        data.card.show()

        data = await convenes.calculator(data)
        print(data.card)

        """data = await convenes.calculator(data)
        for key in data.data:
            icon = await key.get_icon()
            if key.typeRecord == 1:
                print(f"==[{key.resourceType}] ({key.qualityLevel}) {key.name} - {key.time} [{key.drop}]\nICON: {icon.icon}\nBANNER: {icon.banner}\n")
            else:
                print(f"[{key.resourceType}] ({key.qualityLevel}) {key.name} - {key.time}[{key.drop}]\nICON: {icon.icon}\n")
        
        print(f"Total Spin: {data.info.total_spin}\nAstrite: {data.info.astrite}\n==|Five Stars: {data.info.five_stars.resonator} | {data.info.five_stars.weapon}\n==|Four Stars: {data.info.four_stars.resonator} | {data.info.four_stars.weapon}\n==Three Stars: {data.info.three_stars.weapon}")
"""


asyncio.run(main())
