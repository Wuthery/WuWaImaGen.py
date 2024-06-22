# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageFilter
from more_itertools import chunked

import numpy as np

import colorsys
from cachetools import TTLCache

_caches = TTLCache(maxsize=1000, ttl=300)  

async def apply_opacity(image: Image.Image, opacity: float=0.2):
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image

async def light_level(pixel_color: tuple):
    cache_key = pixel_color
    if cache_key in _caches:
        return _caches[cache_key]
    
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3])) 
    _caches[cache_key] = l
    return l

def color_distance(color1, color2):
    return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

async def replace_color(image: Image.Image, old_color: tuple, new_color: tuple, radius: int=100):
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            current_color = pixels[x, y][:3]
            if color_distance(current_color, old_color) <= radius:
                pixels[x, y] = (*new_color, pixels[x, y][3])
    
    return image


async def recolor_image(image: Image.Image, target_color: tuple, light: bool = False):
    if light:
        ll = await light_level(target_color)
        if ll < 45:
            target_color = await get_light_pixel_color(target_color,up = True)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    image = image.copy()

    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if a != 0:
                pixels[i, j] = target_color + (a,)
    if light:
        return image, target_color
    return image

async def get_light_pixel_color(pixel_color: tuple, up: bool = False):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    if up:
        l = min(max(0.6, l), 0.9)
    else:
        l = min(max(0.3, l), 0.8)
    return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
  
async def _get_dark_pixel_color(pixel_color: tuple):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    l = min(max(0.8, l), 0.2)
    a = tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
    
    return  a

async def get_average_color(image: Image.Image):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    channels = image.split()
    
    return (
        round(np.average(channels[0], weights=channels[-1])),
        round(np.average(channels[1], weights=channels[-1])),
        round(np.average(channels[2], weights=channels[-1])),
    )


async def get_dominant_colors(
    image: Image.Image,
    number: int,
    *,
    dither: Image.Quantize = Image.Quantize.FASTOCTREE,
    common: bool =True,
):
    if image.mode != 'RGB':
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        if not common:
            width = image.width
            height = image.height
            
            image = Image.fromarray(np.array([np.repeat(
                np.reshape(image.convert('RGB'), (width * height, 3)),
                np.reshape(image.split()[-1], width * height),
                0,
            )]), 'RGB')
    
    if image.mode == 'RGBA':
        if dither == Image.Quantize.FASTOCTREE:
            simple_image = image.copy()
            simple_image.putalpha(255)
        else:
            simple_image = image.convert('RGB')
    else:
        simple_image = image
    
    reduced = simple_image.quantize(dither=dither, colors=number)
    
    palette = [*chunked(reduced.getpalette(), 3)]
    
    if common and image.mode == 'RGBA':
        alpha = np.array(image.split()[-1])
        
        colors = sorted((
            (
                np.sum(alpha * reduced.point([0] * i + [1] + [0] * (255 - i))),
                tuple(palette[i]),
            )
            for _, i in reduced.getcolors()
        ), reverse=True)
    else:
        colors = [
            (n, tuple(palette[i]))
            for n, i in sorted(reduced.getcolors(), reverse=True)
        ]
    
    return tuple(colors)


async def get_distance_alpha(image: Image.Image, converter=(lambda x: x)):
    width = image.width
    height = image.height
    
    radius = np.hypot(1, 1)
    
    return Image.fromarray(np.fromfunction(
        lambda y, x: np.uint8(255 * converter(np.hypot(
            2 * x / (width - 1) - 1,
            2 * y / (height - 1) - 1,
        ) / radius)),
        (height, width),
    ), 'L')


async def get_background_alpha(image: Image.Image):
    return await get_distance_alpha(
        image,
        lambda x: x * np.sin(x * np.pi / 2),
    )


async def get_foreground_alpha(image: Image.Image):
    return await get_distance_alpha(
        image,
        lambda x: 1 - x * np.sin(x * np.pi / 2),
    )

async def get_colors(image: Image.Image,number,*,common=False,radius=1,quality=None) -> tuple:
    if quality is not None:
        image = image.copy()
        image.thumbnail((quality, quality), 0)
    
    if radius > 1:
        image = image.filter(ImageFilter.BoxBlur(radius))
    
    filtered_image = image.convert('RGB')
    
    if image.mode != 'RGBA':
        filtered_image.putalpha(await get_background_alpha(image))
    else:
        filtered_image.putalpha(Image.fromarray(np.uint8(
            np.uint16(await get_background_alpha(image))
            * image.split()[-1]
            / 255
        ), 'L'))
    
    color_palette = await get_dominant_colors(filtered_image, number, common=common)
    color_palette = color_palette[0][1]
    ll = await light_level(color_palette)
    if ll < 0.15:
        color_palette = await get_light_pixel_color(color_palette)
    elif ll > 0.80:
        color_palette = await _get_dark_pixel_color(color_palette)
        
        
    return color_palette