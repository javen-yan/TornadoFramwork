# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/1/7 下午4:16
"""
from abc import ABC
from web.apps.default.base import BaseRequestHandler, AuthRequestHandler
from web.apps.usercenter.libs.account import login, register
from web.apps.usercenter.libs.profile import get_profile, modify_profile


class LoginHandler(BaseRequestHandler, ABC):

    def post(self):
        response = dict()
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        result = login(self, username, password)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class RegisterHandler(BaseRequestHandler, ABC):

    def post(self):
        response = dict()
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        password2 = self.get_argument('password2', '')
        result = register(self, username, password, password2)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class ProfileHandler(AuthRequestHandler, ABC):

    def get(self):
        response = dict()
        result = get_profile(self)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)

    def put(self):
        phone = self.get_argument('phone', '')
        email = self.get_argument('email', '')
        old_password = self.get_argument('old_password', '')
        new_password = self.get_argument('new_password', '')
        avatar = self.get_argument('avatar', '')
        response = dict()
        result = modify_profile(self, email, phone, old_password, new_password, avatar)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)
