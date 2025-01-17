import glob
import os


def get_path_to_usb_drive():
    usb_drives = []
    out = []
    for i in os.listdir("/Volumes"):
        if i != "Macintosh HD":
            usb_drives.append(i)

    for i in usb_drives:
        for j in glob.glob(f"/Volumes/{i}/**", recursive=True):
            out.append(j)

    return out

