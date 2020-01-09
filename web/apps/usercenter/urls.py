# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/1/7 下午4:05
"""
from web.apps.usercenter.controller import LoginHandler, RegisterHandler, ProfileHandler

urls = [
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/profile', ProfileHandler),
]

