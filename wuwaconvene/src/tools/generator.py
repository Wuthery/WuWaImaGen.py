from collections.abc import Sequence
from pathlib import Path

import kuro
from PIL import Image, ImageDraw

from .color import get_colors, recolor_image
from .model import Calculator, RecordCalculator
from .pill import create_image_with_text, get_font, get_image, resize_image

assets = Path(__file__).parent.parent / "assets"

files = {
    "line": str(assets / "line.png"),
    "frame": str(assets / "frame.png"),
    "background_five": str(assets / "character" / "background_five.png"),
    "shadow_five": str(assets / "character" / "shadow_five.png"),
    "background_four": str(assets / "character" / "background_four.png"),
    "shadow_four": str(assets / "character" / "shadow_four.png"),
    "background_three": str(assets / "character" / "background_three.png"),
    "shadow_three": str(assets / "character" / "shadow_three.png"),
    "count": str(assets / "character" / "count.png"),
    "count_line": str(assets / "character" / "count_line.png"),
    "count_color_line": str(assets / "character" / "count_color_line.png"),
    "five": str(assets / "stars" / "five.png"),
    "four": str(assets / "stars" / "four.png"),
    "three": str(assets / "stars" / "three.png"),
}


line = Image.open(files["line"])
frame = Image.open(files["frame"])


async def open_background(rank):
    if rank == 5:
        return Image.open(files["background_five"]).copy()
    elif rank == 4:
        return Image.open(files["background_four"]).copy()
    else:
        return Image.open(files["background_three"]).copy()


async def open_shadow(rank):
    if rank == 5:
        return Image.open(files["shadow_five"]).copy()
    elif rank == 4:
        return Image.open(files["shadow_four"]).copy()
    else:
        return Image.open(files["shadow_three"]).copy()


async def get_stars(rank):
    if rank == 5:
        return Image.open(files["five"])
    elif rank == 4:
        return Image.open(files["four"])
    else:
        return Image.open(files["three"])


class CardConvene:
    def __init__(
        self, records: Sequence[kuro.models.GachaRecord], banner_name: str = "Other Banner"
    ) -> None:
        self._records = records
        self._banner_name = banner_name
        self._background: Image.Image | None = None

    async def _create_art(self, art: Image.Image) -> None:
        self._background = Image.new("RGBA", (330, 599), (0, 0, 0, 0))
        self._background.alpha_composite(art, (-68, 0))

    async def _create_count(self, value: int, color: tuple[int, int, int, int]) -> Image.Image:
        im = Image.open(files["count"]).copy()
        line = Image.open(files["count_line"])
        color_line = Image.open(files["count_color_line"])
        color_line = await recolor_image(color_line.copy(), color[:3])

        im.alpha_composite(color_line)
        im.alpha_composite(line)

        d = ImageDraw.Draw(im)

        font = get_font(40)
        x = int(font.getlength(str(value)) / 2)
        d.text((46 - x, 26), str(value), font=font, fill=(255, 255, 255, 255))

        return im

    async def create_icons(self, record: kuro.models.GachaRecord):
        background = await open_background(record.rarity)
        shadow = await open_shadow(record.rarity)

        icon = await record.get_icon()
        if record.type == kuro.models.GachaItemType.RESONATOR:
            icon = await get_image(icon.banner, size=(798, 1100))
            background.alpha_composite(icon, (-100, -124))
        else:
            icon = await get_image(icon.icon, size=(414, 414))
            background.alpha_composite(icon, (0, 63))

        background.alpha_composite(shadow)

        count = await self._create_count(record.drop, record.color.rgba)
        background.alpha_composite(count, (325, 386))

        stars = await get_stars(record.rarity)
        background.alpha_composite(stars.resize((143, 32)), (7, 442))

        name = create_image_with_text(record.name, 40, max_width=388, color=(255, 255, 255, 255))
        background.alpha_composite(name, (int(208 - name.size[0] / 2), int(520 - name.size[1] / 2)))

        return background

    async def build(self, color: tuple):
        background = Image.new("RGBA", (1065, 599), color)
        background.alpha_composite(frame)
        background.alpha_composite(self._background)
        line = Image.open(files["line"])
        line, _ = await recolor_image(line.copy(), color, light=True)
        background.alpha_composite(line)

        position_x = 353
        position_y = 69

        for _, key in enumerate(self.icon):
            if _ in [5, 10]:
                position_y += 177
                position_x = 353
            background.alpha_composite(key.resize((115, 158)), (position_x, position_y))

            position_x += 146

        name = create_image_with_text(
            self._banner_name, 20, max_width=217, color=(255, 255, 255, 255)
        )

        background.alpha_composite(name, (353, 15))

        d = ImageDraw.Draw(background)
        font = get_font(21)
        d.text(
            (589, 17),
            f"Total: {self._records.info.total_spin}",
            font=font,
            fill=(255, 255, 255, 255),
        )
        d.text(
            (792, 17), f"5: {self._records.info.next.five}/80", font=font, fill=(255, 255, 255, 255)
        )
        d.text(
            (945, 17), f"4: {self._records.info.next.four}/10", font=font, fill=(255, 255, 255, 255)
        )

        return background

    async def start(self, art: str):
        im = await get_image(art)
        im = resize_image((466, 600), im)
        color = await get_colors(art, 15, common=True, radius=5, quality=800)

        await self._create_art(im)

        self.icon = []
        for i, record in enumerate(self._records):
            if i == 15:
                break

            if record.rarity > 3:
                self.icon.append(await self.create_icons(record))

        return await self.build(color)
