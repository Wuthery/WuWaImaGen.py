<p align="center">
 <img src="https://raw.githubusercontent.com/Wuthery/WuWaConvene.py/main/ReadMeConfig/Banner.png" alt="Баннер"/>
</p>

# WuWaConvene.py
WuWaConvene - A module for Python that allows you to get the gacha history from the game Wuthering Waves, also calculate the guarantors and generate an information card


### Possibilities:

* Get banner history
* Generate card
* Automatically receive a link to the journal
* Counting history

### Helpful information:
* [F.A.Q.](https://github.com/Wuthery/WuWaConvene.py/wiki/Documentation)
* [Discord](https://discord.gg/rKrbqz5utj)

### Install:

```
pip install wuwaconvene
```

### Launch:

```python
import asyncio
import wuwaconvene

async def main():    
    async with wuwaconvene.Convene(link = "YOU_LINK") as convenes:
        data = await convenes.get(1, lang= 'en', generator=True)
        
        data = await convenes.calculator(data)
        for key in data.data:
            icon = await key.get_icon()
            if key.typeRecord == 1:
                print(f"==[{key.resourceType}] ({key.qualityLevel}) {key.name} - {key.time} [{key.drop}]\nICON: {icon.icon}\nBANNER: {icon.banner}\n")
            else:
                print(f"[{key.resourceType}] ({key.qualityLevel}) {key.name} - {key.time}[{key.drop}]\nICON: {icon.icon}\n")
        
        print(f"Total Spin: {data.info.total_spin}\nAstrite: {data.info.astrite}\n==|Five Stars: {data.info.five_stars.resonator} | {data.info.five_stars.weapon}\n==|Four Stars: {data.info.four_stars.resonator} | {data.info.four_stars.weapon}\n==Three Stars: {data.info.three_stars.weapon}")

                
asyncio.run(main())

```


-------
> [!NOTE]  
> The module is still under development, this is not the final version, so stay tuned for updates