import base64

from core.crypto import pbkdf2_hmac_sha1
from core.Rijndael import RijndaelBlock
from core.Slimjson import Slimjson


def parse_saves(save_text) -> tuple[dict, int]:
    if not save_text.strip():
        return {}, 0
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
        print("no saves found for this profile")
    return parsed, i


def decrypt_save(progress_data):
    temp = list(base64.b64decode(progress_data))

    salt = bytes(temp[0:32])
    iv = temp[32:64]
    ciphertext = temp[64:]

    key = pbkdf2_hmac_sha1(b"peekabeyoufoundme", salt, 1000, 32)

    cipher = RijndaelBlock(key, "cbc")
    decrypted = cipher.decrypt(ciphertext, 256, iv)

    padding = decrypted[-1]

    plaintext = bytes(decrypted[: len(decrypted) - padding]).decode("utf-8")

    return plaintext
