# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import json
import os
import aiofiles

class JsonManager:
    def __init__(self, file_path):
        self.file_path = file_path

    async def read(self):
        async with aiofiles.open(self.file_path, mode='r', encoding="utf-8") as file:
            data = await file.read()
            return json.loads(data)

    async def create_directory(self):
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    
    async def write(self, data):
        await self.create_directory()
        
        async with aiofiles.open(self.file_path, mode='w', encoding="utf-8") as file:
            await file.write(json.dumps(data, indent=4, ensure_ascii=False))