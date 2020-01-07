# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/1/7 下午4:28
"""
from abc import ABC

from web.apps.default.base import BaseRequestHandler


class HelloRunner(BaseRequestHandler, ABC):

    def get(self):

        return self.write("hello runner-center")