import platform
import subprocess


def choose_number(message, retry=False, default=1, max_val=999):
    # default only used if retry is false
    while True:
        choice = input(message).strip()
        if choice.isdigit():
            choice = int(choice)
            if choice <= max_val and choice > 0:
                return choice

        if choice:
            string = (
                "Please enter a correct value" if retry else f"Defaulting to {default}"
            )
            print("Invalid input, " + string)

        if retry:
            continue

        return default


def copy_to_clipboard(text):
    system = platform.system()

    if system == "Darwin":
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
    elif system == "Windows":
        subprocess.run(["clip"], input=text.encode(), check=True)
    elif system == "Linux":
        for tool in [["wl-copy"], ["xclip", "-selection", "clipboard"]]:
            try:
                subprocess.run(tool, input=text.encode(), check=True)
                return True
            except FileNotFoundError:
                continue
        print("Clipboard tool not found. Install xclip or wl-clipboard.")
        return False
    return True


def parse_afk_time(afk_time_str: str) -> int:  # seconds
    if afk_time_str == "0":
        return 0
    hours, minutes = afk_time_str.split(":")
    try:
        seconds = int(hours) * 3600 + int(minutes) * 60
    except ValueError:
        print("Invalid time format.")
        return 0
    return seconds
