import platform
import sys
from pathlib import Path

from cli.util import choose_number
from core.saves import parse_saves


def get_save():
    source: int = choose_number(
        message="1. Get saves from Steam profiles \n2. Enter a path manually \n3. Paste save file text\n",
        retry=False,
        default=1,
        max_val=3,
    )
    if source == 1:
        steam_profiles = get_steam_path()
        if len(steam_profiles) != 0:
            choice = choose_number(
                message="Which one do you want to proceed with? ",
                retry=False,
                default=1,
                max_val=len(steam_profiles),
            )

            selected = steam_profiles[choice - 1]

            with open(str(selected), "r") as f:
                save_text = f.read()

        else:
            print("No Steam profiles found.")
            source: int = choose_number(
                message="No Steam profiles found\n 1. Exit \n2. Enter a path manually \n3. Paste save file text\n",
                retry=False,
                default=1,
                max_val=3,
            )
            if source == 1:
                sys.exit()

    if source == 2:
        path: str = input("enter the path manually\n")
        try:
            with open(str(path), "r") as f:
                save_text = f.read()
        except (OSError, ValueError) as e:
            print(f"Failed to read text file: {e}")
            sys.exit()

    if source == 3:
        print(
            "paste the save file text here \n(terminals truncate pastes so might not work)\n"
        )
        save_text = ""
        while True:
            next_line = input()
            if next_line:
                save_text += next_line
            else:
                break
    saves, save_count = parse_saves(save_text)
    if not save_count:
        print("Are you sure you inputted the right save?")
        sys.exit()

    print(
        """
============================
Found the following players:"""
    )
    for i in range(save_count):
        print(f"{i + 1}. {saves[f'save_file_{i}']['player_name']} ")

    chosen_player = choose_number(
        message="Select the player you would like to view the stats for: ",
        retry=False,
        default=1,
        max_val=save_count,
    )

    return saves[f"save_file_{chosen_player - 1}"]


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
        print("Save directory not found")
        return []

    save_files = list(steam_path.glob("*/primary_save.txt"))

    print("""
===================================
Found the following Steam profiles:""")

    for save in save_files:
        print(f"{save_files.index(save) + 1}. {save.absolute()}")

    return save_files
