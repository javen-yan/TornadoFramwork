# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2019/12/5 上午11:50
"""
from abc import ABC
from web.apps.default.base import BaseRequestHandler


class DefaultHandler(BaseRequestHandler, ABC):

    def get(self):
        self.write_json({
            "code": 5000,
            "message": "很抱歉，未找到请求路径"
        })
