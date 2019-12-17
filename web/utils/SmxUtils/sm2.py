# _*_coding:utf-8_*_
"""
@ProjectName: Chaos
@Author:  Javen Yan
@File: SM2.py
@Software: PyCharm
@Time :    2019/11/27 上午11:04
"""
import ctypes
import json
from ctypes import *
import os

current_path = os.path.dirname(os.path.abspath(__file__))

loader = ctypes.cdll.LoadLibrary  # 动态加载库
lib = loader(os.path.join(current_path, 'ICitySMX.so'))


def CreateKeyPair() -> (bool, dict):
    """
    :return:  False, dict() / True, dict:{publicKey:'', privateKey: ''}
    """
    # prepare params
    c_pub_key = c_char_p()
    c_private_key = c_char_p()
    # prepare method
    c_create_key_pair = lib.create_key_pair
    c_create_key_pair.argtypes = [POINTER(c_char_p), POINTER(c_char_p)]
    # do action
    ret = c_create_key_pair(byref(c_pub_key), byref(c_private_key))
    if ret == 0:
        return True, {
            "publicKey": c_pub_key.value.decode(),
            "privateKey": c_private_key.value.decode()
        }
    else:
        False, dict()


def iCitySM2Encrypt(source: bytes, public_key: str) -> (bool, str):
    """
    :param source: bytes
    :param public_key: str
    :return:  False, '' / True, response
    """
    # prepare params
    c_public_key = c_char_p(public_key.encode())
    c_source = c_char_p(source)
    c_length = c_int(len(source))
    c_response = c_char_p()
    # prepare method
    c_city_sm2_encrypt = lib.icity_sm2_encrypt
    c_city_sm2_encrypt.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_char_p)]
    # do action
    ret = c_city_sm2_encrypt(c_public_key, c_source, c_length, byref(c_response))
    if ret == 0:
        return True, replace_ext_str(c_response.value)
    else:
        return False, '加密失败'


def iCitySM2Decrypt(encrypt_data: bytes, private_key: str) -> (bool, str):
    """
    :param encrypt_data: bytes
    :param private_key: str
    :return:  False, '' / True, response
    """
    # prepare params
    c_private_key = c_char_p(private_key.encode())
    c_source = c_char_p(encrypt_data)
    c_clear_length = c_int(0)
    c_clear_str = c_char_p()
    # prepare method
    c_city_sm2_decrypt = lib.icity_sm2_decrypt
    c_city_sm2_decrypt.argtypes = [c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_int)]
    # do action
    ret = c_city_sm2_decrypt(c_private_key, c_source, byref(c_clear_str), byref(c_clear_length))
    if ret == 0:
        return True, replace_ext_str(c_clear_str.value)
    else:
        return False, '解密失败'


def iCitySM2Sign(sign_data: bytes, private_key: str) -> (bool, str):
    """
    :param sign_data: bytes
    :param private_key: str
    :return:  False, '' / True, response
    """
    # prepare params
    c_private_key = c_char_p(private_key.encode())
    c_source = c_char_p(sign_data)
    c_sign_str = c_char_p()
    c_sign_length = c_int(len(sign_data))
    # prepare method
    c_city_sm2_sign = lib.icity_sm2_sign
    c_city_sm2_sign.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_char_p)]
    # do action
    ret = c_city_sm2_sign(c_private_key, c_source, c_sign_length, byref(c_sign_str))
    if ret == 0:
        return True, replace_ext_str(c_sign_str.value)
    else:
        return False, '签名失败'


def iCitySM2Verify(sign_data: bytes, public_key: str, signature: str) -> bool:
    """
    :param sign_data: bytes
    :param public_key: str
    :param signature: str
    :return:  False / True
    """
    # prepare params
    c_public_key = c_char_p(public_key.encode())
    c_source = c_char_p(sign_data)
    c_signature = c_char_p(signature.encode())
    c_sign_length = c_int(len(sign_data))
    # prepare method
    c_city_sm2_sign = lib.icity_sm2_sign
    c_city_sm2_sign.argtypes = [c_char_p, c_char_p, c_int, c_char_p]
    # do action
    ret = c_city_sm2_sign(c_public_key, c_source, c_sign_length, c_signature)
    return ret == 0


def replace_ext_str(data):
    tmp = str(data)
    return tmp.replace('\\xff', '')[2:-1]
