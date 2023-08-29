import os

commands = ["pytube", "aiohttp"]

for i in commands:
    os.system("pip install {}".format(i))