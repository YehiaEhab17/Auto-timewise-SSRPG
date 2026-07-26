import base64
import hashlib
import Rijndael
import platform
from pathlib import Path

def decrypt_save(save):
    start = save.find("progress_data:") + len("progress_data:")
    end =  save.find(",", start)

    progress_data = save[start:end]

    temp = list(base64.b64decode(progress_data))

    salt = bytes(temp[0:32])
    iv = temp[32:64]
    ciphertext = temp[64:]

    key = hashlib.pbkdf2_hmac("sha1", b'peekabeyoufoundme', salt, 1000, 32)

    cipher = Rijndael.RijndaelBlock(key, 'cbc')
    decrypted = cipher.decrypt(ciphertext, 256, iv)

    padding = decrypted[-1]

    plaintext = bytes(decrypted[:len(decrypted)-padding]).decode("utf-8")

    print(plaintext)
    return plaintext

def start():
    print("hello!!!!!!! world!!!!!!!!")
    print(f"you use {platform.system()}")
    get_steam_save()


# Windows: C:/Users/userName/AppData/LocalLow/Martian Rex, Inc_/Stone Story/(steam id)/primary_save.txt
  
# MacOS: ~/Library/Application Support/Martian Rex, Inc_/Stone Story/(steam id)/primary_save.txt
  
# Linux: (your Steam install location for SSRPG)/Martian Rex, Inc_/Stone Story/(steam id)/primary_save.txt
# typical install location: ~/.local/share/Steam/steamapps/common/Stone Story RPG/
def get_steam_save():
    os_name = platform.system()

    if os_name == "Linux":
        TYPICAL = Path.home() / ".local/share/Steam/steamapps/common/Stone Story RPG/"
        steam_path = TYPICAL / "Martian Rex, Inc_/Stone Story/"

    elif os_name == "Darwin": 
        steam_path = Path.home() / "Library/Application Support/Martian Rex, Inc_/Stone Story/"
    elif os_name == "Windows":
        steam_path = Path.home() / "AppData/LocalLow/Martian Rex, Inc_/Stone Story/"
    else:
        print(f"Unsupported operating system: {os_name}")
        return None

    if not steam_path.exists():
        print("save directory not found")
        return None
    
    save_files = list(steam_path.glob("*/primary_save.txt"))

    for save in save_files:
        print(f"found save at {save.absolute}")

    return save_files

if __name__ == "__main__":
    start()

