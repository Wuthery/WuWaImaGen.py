import json
from io import BytesIO
from pathlib import Path
from typing import Literal

import aiohttp
from cachetools import TTLCache
from PIL import Image, ImageDraw, ImageFont

cache = TTLCache(maxsize=1000, ttl=300)
assets = Path(__file__).parent.parent / "assets"


def get_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(assets / "font" / "font_hsr.ttf"), size)


async def download_image(url: str) -> bytes:
    headers = {"referer": "https://www.pixiv.net/"} if "pximg" in url else None
    async with aiohttp.ClientSession(headers=headers) as session, session.get(url) as r:
        return await r.read()


async def get_image(
    url: str, *, size: tuple[int, int] | None = None, thumbnail_size: tuple[int, int] | None = None
) -> Image.Image:
    cache_key = json.dumps((url, size, thumbnail_size), sort_keys=True)

    if cache_key in cache:
        return cache[cache_key]

    bytes_ = await download_image(url)

    im = Image.open(BytesIO(bytes_)).convert("RGBA")
    if size is not None:
        im = im.resize(size)
    if thumbnail_size is not None:
        im.thumbnail(thumbnail_size)

    cache[cache_key] = im
    return im


def resize_image(size: tuple[int, int], image: Image.Image) -> Image.Image:
    """Resize image to fit the size, keeping the aspect ratio."""
    background_image = Image.new("RGBA", size, color=(0, 0, 0, 0))
    foreground_image = image.convert("RGBA")

    scale = max(size[0] / foreground_image.size[0], size[1] / foreground_image.size[1])
    foreground_image = foreground_image.resize(
        (int(foreground_image.size[0] * scale), int(foreground_image.size[1] * scale))
    )

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2

    if foreground_size[1] > background_size[1]:
        y_offset = max(
            int(0.3 * (foreground_size[1] - background_size[1])), int(0.5 * (-foreground_size[1]))
        )
        y = -y_offset
    else:
        y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image


def create_image_with_text(
    text: str,
    font_size: int,
    max_width: int = 336,
    color: tuple[int, int, int, int] = (255, 255, 255, 255),
    allignment: Literal["left", "center"] = "left",
) -> Image.Image:
    cache_key = json.dumps((text, font_size, max_width, color, allignment), sort_keys=True)
    if cache_key in cache:
        return cache[cache_key]

    font = get_font(font_size)

    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = [*line, word]
            temp_text = " ".join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(" ".join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(" ".join(line)).getbbox()[3]

    img = Image.new("RGBA", (min(width, max_width), height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)

    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(" ".join(line)).getbbox()[2:]
        x_text = (max_width - text_width) // 2 if allignment == "center" and line_num > 0 else 0
        draw.text((x_text, y_text), " ".join(line), font=font, fill=color)
        y_text += text_height + 5

    cache[cache_key] = img

    return img
