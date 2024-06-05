# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import aiofiles
import asyncio
import os
import re
from typing import Union
from pathlib import Path
from .json_data import JsonManager

json_data_path = Path(__file__).parent.parent / "assets" / "character_icon.json"

async def get_data_resonator(resonator_id: Union[str, int]) -> dict:
    try:
        json_data = await JsonManager(json_data_path).read()
    except asyncio.CancelledError:
        raise 
    except Exception as e:
        raise Exception(f"Error reading data: {e}")

    if str(resonator_id) in json_data:
        return json_data[str(resonator_id)]
    
    url = f"https://api.hakush.in/ww/data/en/character/{resonator_id}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if not str(resonator_id) in json_data:
                    json_data[str(resonator_id)] = {"Icon": data["Icon"], "Background": data["Background"]}
                    await JsonManager(json_data_path).write(json_data)
                    
                return data
            else:
                response_text = await response.text()
                print(f"Error: {response_text}")
                return None

async def fetch_data(payload: dict) -> dict:
    url = "https://gmserver-api.aki-game2.net/gacha/record/query"
    headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                response_text = await response.text()
                print(f"Error: {response_text}")
                return None

async def auto_link(game_path):
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
    