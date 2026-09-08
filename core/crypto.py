import hashlib
import hmac


def pbkdf2_hmac_sha1(password, salt, iterations, dk_len):
    hlen = 20
    blocks = (dk_len + hlen - 1) // hlen

    derived = b""
    for index in range(1, blocks + 1):
        u = hmac.new(password, salt + index.to_bytes(4, "big"), hashlib.sha1).digest()

        result = u
        for _ in range(1, iterations):
            u = hmac.new(password, u, hashlib.sha1).digest()
            result = bytes(a ^ b for a, b in zip(result, u))

        derived += result

    return derived[:dk_len]
