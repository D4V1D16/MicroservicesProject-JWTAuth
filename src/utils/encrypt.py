from cryptography.fernet import Fernet
from utils.storageKey import loadKey
encryptionKey = loadKey()

key = Fernet(encryptionKey)

def encrypt(psswrd):
    encrypted_password = key.encrypt(psswrd.encode('utf-8'))
    return encrypted_password

def decryptPassword(psswrd):
    return key.decrypt(psswrd)