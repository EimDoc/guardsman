import asyncio
import glob
import os

from src.config import PATH_TO_USB


def get_path_to_usb_drive():
    usb_drives = []
    out = []
    for i in os.listdir(PATH_TO_USB):
        if i != "Macintosh HD":
            usb_drives.append(i)

    for i in usb_drives:
        for j in glob.glob(f"{PATH_TO_USB}/{i}/**", recursive=True):
            out.append(j)

    return out


async def test_generator():
    text = ["data:Say\n\n", "data:hello\n\n", "data:to\n\n", "data:world\n\n", "data:Say\n\n", "data:hello\n\n", "data:to\n\n", "data:world\n\n", "data:Say\n\n", "data:hello\n\n", "data:to\n\n", "data:world\n\n", "data:Say\n\n", "data:hello\n\n", "data:to\n\n", "data:world\n\n"]
    for i in text:
        yield i
        await asyncio.sleep(0.5)
