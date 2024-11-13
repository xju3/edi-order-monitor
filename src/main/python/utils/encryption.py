import hashlib


def md5(val):
    r = hashlib.md5(val.encode())
    return r.hexdigest()
