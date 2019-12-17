# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: main.py
@Software: PyCharm
@Time :    2019/12/5 上午11:50
"""
from abc import ABC
from web.libs.auth.auth_libs import auth_login
from web.views.base import AuthRequestHandler, BaseRequestHandler, make_response


class LoginHandler(BaseRequestHandler, ABC):

    def get(self):
        return self.write_json({"code": "0000", "msg": "login page"})

    def post(self):
        payload = self.get_payload()
        res = auth_login(self, **payload)
        return self.write_json(make_response(**res))


class MainHandler(AuthRequestHandler, ABC):

    def get(self):
        return self.write_encrypt_data({"code": "0000", "msg": "main page"})


class DefaultHandler(BaseRequestHandler, ABC):

    def get(self):
        self.set_status(404)
        self.write_json({
            "code": 5000,
            "msg": "Api Backend Not Found This Route"
        })
