import base64
import hashlib
import platform
from pathlib import Path

import Rijndael
from Slimjson import Slimjson
from util import choose_number


def get_save():
    steam_profiles = get_steam_path()
    selected = None
    source: bool = choose_number(
        message="1. steam save\n2. manual path \n3. save file text \n(default is steam save)",
        retry=False,
        default=1,
        max=3,
    )
    if source == 1:
        if len(steam_profiles) != 0:
            choice = choose_number(
                message="choose a steam profile (enter the number, defaults to the first one",
                retry=False,
                default=0,
                max=len(steam_profiles),
            )

            selected = steam_profiles[choice]

            with open(str(selected), "r") as f:
                save_text = f.read()

        else:
            print("no saves (steam profile) found, input path or save?")
            # TODO: IMPLEMENT THIS
    elif source == 2:
        path: Path = input("enter the path manually")
        with open(str(path), "r") as f:
            save_text = f.read()
    elif source == 3:
        pass
        # TODO IMPLEMENT THIS

    saves, save_count = parse_saves(save_text)

    for i in range(save_count):
        print(f"{i}. {saves[f'save_file_{i}']['player_name']} ")
    chosen_player = choose_number(
        message="select the player you would like to view the stats for (defaults to first)",
        retry=False,
        default=0,
        max=save_count,
    )

    return saves[f"save_file_{chosen_player}"]


def parse_saves(save_text) -> tuple[dict, int]:
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
        return []

    if not steam_path.exists():
        print("save directory not found")
        return []

    save_files = list(steam_path.glob("*/primary_save.txt"))

    for save in save_files:
        print(f"{save_files.index(save) + 1}. found save at {save.absolute()}")

    return save_files
