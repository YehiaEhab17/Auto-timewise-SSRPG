import base64
import hashlib
import platform
import re
from dataclasses import dataclass
from pathlib import Path

import Rijndael
from Slimjson import Slimjson

# LOCATIONS = {
#     "rocky_plateau": "Rocky Plateau",
#     "deadwood_valley": "Deadwood Canyon",
#     "caustic_caves": "Caves of Fear",
#     "fungus_forest": "Mushroom Forest",
#     "undead_crypt": "Haunted Halls",
#     "bronze_mine": "Boiling Mine",
#     "icy_ridge": "Icy Ridge",
#     "temple": "Temple",
# }


# {'id': 'caustic_caves3', 'bT': 1112.0, 'aT': 1811.661, 'aHl': 20.82896, 'aHg': 0.0, 'aKg': 13.34721, 'aXg': 17.55122, 'aRg': 154.8184, 'd': 754.3131}
@dataclass
class LocationStats:
    loc_id: str  # loc id e.g caustic_caves3
    name: str
    stars: int
    bT: float  # best time in frames
    aT: float  # average time in frames
    aHl: float  # average health lost
    aHg: float  # average health gain
    net_hp: float
    aKg: float  # average ki gain
    aXg: float  # average xp gain?
    aRg: float  # average resource gain
    d: float  # damage?
    # todo: maybe implement stuff for eent resources


def start():
    save: dict

    print("hello!!!!!!! world!!!!!!!!")
    print(f"you use {platform.system()}")
    # todo: add actual UX

    saves = get_steam_path()
    selected = None

    if saves is None or len(saves) == 0:
        print("no saves found, input path?")
        return
        # todo: allow user to input path or paste the full save

    else:
        choice = input(
            "choose a steam profile (enter the number, defaults to the first one)"
        ).strip()

        try:
            selected = saves[int(choice)]
        except (ValueError, IndexError):
            print("selecting the first steam profile")
            selected = saves[0]

        with open(str(selected), "r") as f:
            save_text = f.read()

        save, save_count = get_saves(save_text)

    # todo: let them choose which save to proceed with
    print(save_count)
    locations: dict[tuple[str, int], LocationStats] = {}
    get_location_times(save, locations)

    print(locations)
    # path 1: get the optimal stats direclty here
    # path 2: output to timewise (local / web)
    # path 3: get a copy paste for timewise

    # todo extract logic from timewise


def get_saves(save_text) -> tuple[dict, int]:
    parser = Slimjson()
    parsed: dict = parser.parse(save_text)

    i = 0
    while True:
        if f"save_file_{i}" not in parsed:
            break
        progress_data_e = parsed[f"save_file_{i}"]["progress_data"]
        progress_data_d = decrypt_save(progress_data_e)

        parsed[f"save_file_{i}"]["progress_data"] = parser.parse(progress_data_d)
        parsed[f"save_file_{i}"]["progress_data"]["encrypted"] = False
        i += 1

    if i == 0:
        print("no saves found for this steam profile")
    return parsed, i


def decrypt_save(progress_data):
    temp = list(base64.b64decode(progress_data))

    salt = bytes(temp[0:32])
    iv = temp[32:64]
    ciphertext = temp[64:]

    key = hashlib.pbkdf2_hmac("sha1", b"peekabeyoufoundme", salt, 1000, 32)

    cipher = Rijndael.RijndaelBlock(key, "cbc")
    decrypted = cipher.decrypt(ciphertext, 256, iv)

    padding = decrypted[-1]

    plaintext = bytes(decrypted[: len(decrypted) - padding]).decode("utf-8")

    return plaintext


def get_location_times(save, locations):
    stats: list = save["save_file_0"]["progress_data"]["quest_data"]["stats"]

    for location in stats:
        match = re.match(r"^([a-zA-Z_]+)(\d+)$", location["id"])

        if match:
            name, stars = match.groups()
        else:
            continue

        aHg_val = location.get("aHg", 0.0)
        aHl_val = location.get("aHl", 0.0)

        loc_stats = LocationStats(
            loc_id=location["id"],
            name=name,
            stars=int(stars),
            bT=location.get("bT", 0.0),
            aT=location.get("aT", 0.0),
            aHl=aHl_val,
            aHg=aHg_val,
            net_hp=aHg_val - aHl_val,
            aKg=location.get("aKg", 0.0),
            aXg=location.get("aXg", 0.0),
            aRg=location.get("aRg", 0.0),
            d=location.get("d", 0.0),
        )
        locations[(name, stars)] = loc_stats


# Windows: C:/Users/userName/AppData/LocalLow/Martian Rex, Inc_/Stone Story/(steam id)/primary_save.txt
#
# MacOS: ~/Library/Application Support/Martian Rex, Inc_/Stone Story/(steam id)/primary_save.txt
#
# Linux: (your Steam install location for SSRPG)/Martian Rex, Inc_/Stone Story/(steam id)/primary_save.txt
# typical install location: ~/.local/share/Steam/steamapps/common/Stone Story RPG/
#
def get_steam_path():
    os_name = platform.system()

    if os_name == "Linux":
        TYPICAL = Path.home() / ".local/share/Steam/steamapps/common/Stone Story RPG"
        steam_path = TYPICAL / "Martian Rex, Inc_/Stone Story"

    elif os_name == "Darwin":
        steam_path = (
            Path.home() / "Library/Application Support/Martian Rex, Inc_/Stone Story"
        )
    elif os_name == "Windows":
        steam_path = Path.home() / "AppData/LocalLow/Martian Rex, Inc_/Stone Story"
    else:
        print(f"Unsupported operating system: {os_name}")
        return None

    if not steam_path.exists():
        print("save directory not found")
        return None

    save_files = list(steam_path.glob("*/primary_save.txt"))

    for save in save_files:
        print(f"{save_files.index(save) + 1}. found save at {save.absolute()}")

    return save_files


if __name__ == "__main__":
    start()
