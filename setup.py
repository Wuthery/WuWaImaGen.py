import setuptools
import re

with open('wuwaconvene/__init__.py') as f:
	"""
		Get version from utils.py
		Ref: https://github.com/Rapptz/discord.py/blob/52f3a3496bea13fefc08b38f9ed01641e565d0eb/setup.py#L9
	"""
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)

setuptools.setup(
	name="wuwaconvene",
	version=version,
	author="DeviantUa",
	author_email="deviantapi@gmail.com",
	description= "WuWaConvene - A module for Python that allows you to get the gacha history from the game Wuthering Waves, also calculate the guarantors and generate an information card",
	long_description=open("README.md", "r", encoding="utf-8").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/DEViantUA/StarRailCard",
	keywords = ["honkai", "cards", "generation", "honkaistarraill","raill", "starraill", "builds", "honkairail", "honkai"] ,
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"pydantic",
		"aiohttp",
		"cachetools",
        "Pillow",
        "aiofiles",
        "imageio",
        "moviepy",
        "more-itertools",
        "numpy",
        "beautifulsoup4",
        "anyio"
	],
	python_requires=">=3.9",
	include_package_data=True
)