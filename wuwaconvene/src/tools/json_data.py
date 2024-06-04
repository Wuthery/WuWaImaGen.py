# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import aiofiles

if TYPE_CHECKING:
    from pathlib import Path


class JsonManager:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    async def read(self) -> dict[str, Any]:
        async with aiofiles.open(self._file_path, mode="r", encoding="utf-8") as file:
            data = await file.read()
            return json.loads(data)

    async def write(self, data: dict[str, Any]) -> None:
        async with aiofiles.open(self._file_path, mode="w", encoding="utf-8") as file:
            await file.write(json.dumps(data, indent=4, ensure_ascii=False))
