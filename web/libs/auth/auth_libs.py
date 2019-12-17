# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: auth_libs.py
@Software: PyCharm
@Time :    2019/12/5 上午11:38
"""
import time
from uuid import uuid4
import jwt
from jwt import ExpiredSignatureError
from web.settings import *
from logzero import logger


def auth_login(self, **kwargs):
    need_key = ['username', 'password']
    if not kwargs:
        return {'status': False, 'msg': '参数不能为空'}
    for k, v in kwargs.items():
        if k not in need_key:
            return {'status': False, 'msg': '缺少参数 {}, 请补全后重试'.format(k)}
        elif not v:
            return {'status': False, 'msg': '参数 {} 不能为空, 请补全后重试'.format(k)}
    username = kwargs.get('username')
    password = kwargs.get('password')
    if username != 'admin':
        return {'status': False, 'msg': '未找到该用户'}
    if password != 'admin':
        return {'status': False, 'msg': '密码不正确'}
    payload = {
        'id': str(uuid4()),
        'uuid': str(uuid4()),
        'username': username,
        'exp': time.time() + sys_jwt_expire
    }
    token = jwt.encode(payload, sys_secret, algorithm='HS256')
    return {'status': True, 'msg': '认证成功', 'data': {'token': token.decode('utf-8'), 'username':  username}}


def decode_jwt(self, token):
    try:
        res = jwt.decode(jwt=token, key=sys_secret, algorithm='HS256', verify=True)
        return {'status': True, 'msg': 'Token校验成功', 'data': res}
    except ExpiredSignatureError:
        return {'status': False, 'msg': 'Token已经过期'}
