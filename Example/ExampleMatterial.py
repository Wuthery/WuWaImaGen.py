import asyncio
import wuwaimagen
from wuwaimagen import (
    MaterialWeapon,
    MaterialCharacter,
    Level,
    StatBonus,
    StatBonusAttackLevel,
    StatBonusResonatorSkill,
    StatBonusResonanceLiberation,
    StatBonusIntroSkill,
    StatBonusForteCircuit
    )

'''
This example serves as an example of material cards for upgrading a character and weapons
More examples here: https://github.com/Wuthery/WuWaImaGen.py/tree/main/Example
'''

client = wuwaimagen.ClientWuWa(assets=True)

config_weapon = MaterialWeapon(
    id = 21040015,
    level= Level(max= 90)
)

config_character = MaterialCharacter(
        id=1301,
        level= Level(min=10, max=90),
        normal_attack=Level(min=1, max=10),
        resonator_skill=Level(min=1, max=10),
        resonance_liberation=Level(min=1, max=10),
        intro_skill = Level(min=1, max=10),
        forte_circuit = Level(min=1, max=10),
        stat_bonus = StatBonus(
            attack_level = StatBonusAttackLevel.full,
            resonator_skill = StatBonusResonatorSkill.full,
            resonance_liberation = StatBonusResonanceLiberation.full,
            intro_skill = StatBonusIntroSkill.full,
            forte_circuit = StatBonusForteCircuit.full
        )
    )

async def main():    
    async with client:
        
        data = await client.get_material(
            config_character,
            card= True
            )
            
        if data.character is None:
            print(f"{data.weapon.name} | R{data.weapon.rarity}")
            print("=======Items======")
            for key in data.items:
                items = data.items.get(key)
                print(f"[{items.id}] - R{items.rarity} | Value: {items.value}")
                print(f"Icon: {items.icon}")
             
            print(f"\nCard: {data.card}")
        else:
            print(f"{data.character.name} | R{data.character.rarity}")
            print("=======Items======")
            for key in data.items:
                items = data.items.get(key)
                print(f"[{items.id}] - R{items.rarity} | Value: {items.value}")
                print(f"Icon: {items.icon}")
            
            print(f"\nCard: {data.card}")
                
asyncio.run(main())
