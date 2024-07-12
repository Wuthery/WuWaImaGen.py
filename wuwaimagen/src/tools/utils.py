# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import aiofiles
import json
import os
import re
from ..settings.other import WUTHERY_CDN, json_local
from .json_data import JsonManager
from ..model.material import (
    StatBonusForteCircuit,
    StatBonusAttackLevel,
    StatBonusResonatorSkill,
    StatBonusResonanceLiberation,
    StatBonusIntroSkill
)

async def get_textMap(lang: str = "en", filename: str = "MultiText") -> dict:
    url = f"https://raw.githubusercontent.com/Dimbreath/WutheringData/master/TextMap/{lang}/{filename}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = json.loads(await response.text())
                await JsonManager(json_local / lang / f'{filename}.json').write(data)
                return data
            else:
                print(f"Error: {await response.text()}")
                return None

async def get_data_resonator(filename: str = "RoleInfo") -> dict:
    url = WUTHERY_CDN + f"d/GameData/ConfigDBParsed/{filename}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                await JsonManager(json_local / f'{filename}.json').write(data)
                return data
            else:
                print(f"Error: {await response.text()}")
                return None


async def get_data(lang: str = "en", catalog: str = "en", filename: str = "RoleInfo") -> dict:
    url = WUTHERY_CDN + f"d/GameData/Grouped/localized/{lang}/{catalog}/{filename}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                await JsonManager(json_local / lang / catalog / f'{filename}.json').write(data)
                return data
            else:
                print(f"Error: {await response.text()}")
                return None

async def get_open_file(filename: str = 'RoleInfo.json') -> dict:
    try:
        return await JsonManager(json_local / filename).read()
    except Exception as e:
        return {}
                
async def get_event_list(payload: dict) -> dict:
    url = "https://aki-gm-resources-back.aki-game.net/gamenotice/G153/6eb2a235b30d05efd77bedb5cf60999e/notice.json"
    headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                response_text = await response.text()
                print(f"Error: {response_text}")
                return None

async def auto_link(game_path: str) -> str:
    try:
        game_path = game_path.split("Wuthering Waves")[0]
        log_file = os.path.join(game_path, 'Wuthering Waves', 'Wuthering Waves Game', 'Client', 'Saved', 'Logs', 'Client.log')

        if not os.path.exists(log_file):
            raise Exception("The file '{}' does not exist.".format(log_file))

        async with aiofiles.open(log_file, mode='r', encoding='utf-8') as file:
            log_content = await file.read()

            latest_url_entry = None
            for line in reversed(log_content.splitlines()):
                if "https://aki-gm-resources-oversea.aki-game.net" in line:
                    latest_url_entry = line
                    break

            if latest_url_entry:
                url_pattern = 'url":"(.*?)"'
                url_match = re.search(url_pattern, latest_url_entry)
                if url_match:
                    url = url_match.group(1)
                    return url
                else:
                    raise Exception("No URL found.")
            else:
                raise Exception("No matching entries found in the log file. Please open your Convene History first!")
    except Exception as e:
        raise Exception("An error occurred: {}".format(e))

link_icon = "https://files.wuthery.com/p/GameData/UIResources/Common/Image"

conditions = {
    4: [StatBonusForteCircuit, [1,3]],
    5: [StatBonusForteCircuit, [2,3]],
    41: [StatBonusAttackLevel, [1, 3]],
    45: [StatBonusAttackLevel, [2, 3]],
    42: [StatBonusResonatorSkill, [1, 3]],
    46: [StatBonusResonatorSkill, [2, 3]],
    43: [StatBonusResonanceLiberation, [1, 3]],
    47: [StatBonusResonanceLiberation, [2, 3]],
    44: [StatBonusIntroSkill, [1, 3]],
    48: [StatBonusIntroSkill, [2, 3]]
}


def get_breach_level(level):
    if level < 20:
        return 0
    elif level < 40:
        return 1
    elif level < 50:
        return 2
    elif level < 60:
        return 3
    elif level < 70:
        return 4
    elif level < 80:
        return 5
    elif level <= 90:
        return 6
    

def sort_items(data):
    sorted_keys = sorted(data.keys(), key=int)
    sorted_data = {key: data[key] for key in sorted_keys}
    
    return sorted_data


def status_stat_bonus(parent_nodes, stat_bonus):
    condition = conditions.get(parent_nodes)
    if condition:
        class_type, values = condition
        for stat in stat_bonus:
            if isinstance(stat, class_type) and stat.value not in values:
                return False
            
    return True