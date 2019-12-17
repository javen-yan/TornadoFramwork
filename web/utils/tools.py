import base64
import socket
from web.utils.SmxUtils import iCitySM2Encrypt, iCitySM2Decrypt
from web.settings import sys_public_key, sys_private_key, sys_aes_key, sys_aes_iv
from Crypto.Cipher import AES


def machine_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    try:
        return s.getsockname()[0]
    finally:
        s.close()


def decrypt_data(data):
    """解密数据"""
    state, res = iCitySM2Decrypt(data, private_key=sys_private_key)
    if state:
        return res
    else:
        return ''


def encrypt_data(data):
    """加密数据"""
    state, res = iCitySM2Encrypt(data, public_key=sys_public_key)
    if state:
        return res
    else:
        return ''


class AesCrypto:
    def __init__(self, key, IV):
        self.key = key
        self.iv = IV
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        crypto = AES.new(self.key, self.mode, self.iv)
        length = 16
        pad = lambda s: s + ((length - len(s) % length) * chr(length - len(s) % length)).encode()
        r = crypto.encrypt(pad(text))
        return base64.b64encode(r)

    def decrypt(self, text):
        text = base64.b64decode(text)
        unpad = lambda s: s[0:-s[-1]]
        crypto = AES.new(self.key, self.mode, self.iv)
        plain_text = unpad(crypto.decrypt(text)).decode()
        return plain_text


aes_tools = AesCrypto(key=sys_aes_key, IV=sys_aes_iv)