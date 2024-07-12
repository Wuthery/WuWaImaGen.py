# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import json
import aiohttp
from cachetools import TTLCache
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from ..settings.other import assets_local
cache = TTLCache(maxsize=1000, ttl=300)  


async def get_font(size:int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(assets_local / 'font' / 'font_hsr.ttf'), size)

async def get_download_img(link: str,size:tuple = None, thumbnail_size: tuple= None):
    cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)
        
    if cache_key in cache:
        return cache[cache_key]
    headers_p = {}
    try:
        if "pximg" in link:
            headers_p = {
                "referer": "https://www.pixiv.net/",
            }
        async with aiohttp.ClientSession(headers=headers_p) as session, session.get(link) as r:
            image = await r.read()
    except Exception as e:
        raise Exception (f"Error image: {link}")
    
    image = Image.open(BytesIO(image)).convert("RGBA")
    if size:
        image = image.resize(size)
        cache[cache_key] = image
        return image
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        cache[cache_key] = image
        return image
    else:
        cache[cache_key] = image
        return image
    
async def get_center_size(size: tuple, image: Image.Image) -> Image.Image:
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = image.convert("RGBA")

    scale = max(size[0] / foreground_image.size[0], size[1] / foreground_image.size[1])
    foreground_image = foreground_image.resize((int(foreground_image.size[0] * scale), int(foreground_image.size[1] * scale)))

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2

    if foreground_size[1] > background_size[1]:
        y_offset = max(int(0.3 * (foreground_size[1] - background_size[1])), int(0.5 * (-foreground_size[1])))
        y = -y_offset
    else:
        y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image


async def create_image_with_text(text: str, font_size: int, max_width: int = 336, color: tuple = (255, 255, 255, 255), alg: str = "Left") -> Image.Image:
    cache_key = json.dumps((text, font_size, max_width, color, alg), sort_keys=True)
    if cache_key in cache:
        return cache[cache_key]
    
    font = await get_font(font_size)

    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
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
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    img = Image.new('RGBA', (min(width, max_width), height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    
    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        if alg == "center" and line_num > 0:
            x_text = (max_width - text_width) // 2
        else:
            x_text = 0
        draw.text((x_text, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5
        
    cache[cache_key] = img
    
    return img


def calculate_text_size(text, font, max_width):
    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getbbox(temp_text)[2] - font.getbbox(temp_text)[0]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    max_line_width = max(font.getbbox(' '.join(line))[2] - font.getbbox(' '.join(line))[0] for line in lines)
    total_height = sum(font.getbbox(' '.join(line))[3] - font.getbbox(' '.join(line))[1] for line in lines) + (len(lines) - 1) * 5

    return lines, min(max_line_width, max_width), total_height

async def create_image_with_text_v2(text: str, font_size: int, max_width: int = 336, color: tuple = (255, 255, 255, 255), padding_default:tuple = (0,0), alg: str = "Left") -> Image.Image:
    cache_key = json.dumps((text, font_size, max_width, color, alg), sort_keys=True)
    if cache_key in cache:
        return cache[cache_key]
    
    font = await get_font(font_size)

    lines, width, height = calculate_text_size(text, font, max_width)

    padding = 5
    img_width = width + 2 * padding + padding_default[0]
    img_height = height + 2 * padding + padding_default[1]

    img = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    y_text = padding
    for line in lines:
        line_text = ' '.join(line)
        bbox = font.getbbox(line_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if alg.lower() == "center":
            x_text = (img_width - text_width) // 2
        else:
            x_text = padding
        draw.text((x_text, y_text), line_text, font=font, fill=color)
        y_text += text_height + 5

    cache[cache_key] = img
    
    return img

async def apply_opacity(image, opacity=0.2):
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image