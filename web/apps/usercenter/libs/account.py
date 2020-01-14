# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: account.py
@Software: PyCharm
@Time :    2020/1/8 下午4:52
"""
import time
from datetime import datetime

import jwt
from jwt import ExpiredSignatureError
from logzero import logger

from web.models.databases import AccountModel
from web.apps.default.globalstatus import UserCenterStatusCode
from web.settings import sys_secret, sys_jwt_expire


def register(self, name, password, password2):
    name = name.strip()
    password = password.strip()
    password2 = password2.strip()
    if name == '' and password == '':
        return {'status': False, 'msg': '请输入用户名或密码', 'code': UserCenterStatusCode.account_error.value}
    if password != password2:
        return {'status': False, 'msg': '输入密码不一致', 'code': UserCenterStatusCode.not_match_error.value}
    user = AccountModel()
    user.username = name
    user.password = password
    self.db.add(user)
    self.db.commit()
    return {'status': True, 'msg': '注册成功', 'code': UserCenterStatusCode.success.valueSSS}


def login(self, name, password):
    if name == '' and password == '':
        return {'status': False, 'msg': '请输入用户名或密码', 'code': UserCenterStatusCode.account_error.value}
    user = AccountModel.by_name(name)  # 注意
    if user and user.auth_password(password):  # 注意
        user.updated_at = datetime.now()
        self.db.add(user)
        self.db.commit()
        payload = {
            'id': user.id,
            'uuid': user.uuid,
            'username': user.username,
            'expired': time.time() + sys_jwt_expire
        }
        token = gen_token(payload)
        info = user.to_dict()
        info['token'] = token
        return {'status': True, 'msg': '登录成功', 'code': UserCenterStatusCode.success.value, 'data': info}
    return {'status': False, 'msg': '用户名输入错误或者密码不正确', 'code': UserCenterStatusCode.account_error.value}


def gen_token(payloads):
    token = jwt.encode(payloads, sys_secret, algorithm='HS256')
    return token.decode('utf-8')


def decode_jwt(self, token):
    try:
        result = jwt.decode(jwt=token, key=sys_secret, algorithm='HS256', verify=True)
        return {'status': True, 'msg': 'Token校验成功', 'data': result, 'code': UserCenterStatusCode.success.value}
    except ExpiredSignatureError:
        return {'status': False, 'msg': 'Token已经过期', "code": UserCenterStatusCode.token_expired_error.value}