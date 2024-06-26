
def loadKey():
    with open('fernet_key.txt', 'rb') as f:
        key = f.read()
        return key