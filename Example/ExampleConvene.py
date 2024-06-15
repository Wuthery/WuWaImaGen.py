import asyncio
import wuwaimagen

'''
This example allows you to generate a gacha card and calculate your luck.
More examples here: https://github.com/Wuthery/WuWaImaGen.py/tree/main/Example
'''

ClientWuWa = wuwaimagen.ClientWuWa(assets=True)

async def main():
    link = "https://aki-gm-resources-oversea.aki-game.net/aki/gacha/index.html#/record?svr_id=6eb2a235b30d05efd77bedb5cf60999e&player_id=600329448&lang=en&gacha_id=4&gacha_type=6&svr_area=global&record_id=97bfb175262ffb96a20874040b8662be&resources_id=917dfa695d6c6634ee4e972bb9168f6a"
    #link = await wuwaconvene.auto_link("D:\Wuthering Waves") - Alternative automatic way to receive a link
    
    async with ClientWuWa as client:
        data = await client.get_gacha_info(link, 1, lang= 'en', generator=True)
        for key in data.data:
            icon = await key.get_icon()
            if key.typeRecord == 1:
                print(f"==[{key.resourceType}] ({key.qualityLevel}) {key.name} - {key.time} [{key.drop}]\nICON: {icon.icon}\nBANNER: {icon.banner}\n")
            else:
                print(f"[{key.resourceType}] ({key.qualityLevel}) {key.name} - {key.time}[{key.drop}]\nICON: {icon.icon}\n")
        print(f"Total Spin: {data.info.total_spin}\nAstrite: {data.info.astrite}\n==|Five Stars: {data.info.five_stars.resonator} | {data.info.five_stars.weapon}\n==|Four Stars: {data.info.four_stars.resonator} | {data.info.four_stars.weapon}\n==Three Stars: {data.info.three_stars.weapon}")
        print(f"Card: {data.card}")
      
asyncio.run(main())
