import base64
import hashlib
import Rijndael


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


if __name__ == "__main__":
    start()

