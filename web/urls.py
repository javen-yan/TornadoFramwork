# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2019/12/5 上午10:41
"""
from web.views.main import MainHandler, DefaultHandler

urlpatterns = [
    (r'/api/v1/index', MainHandler),
    (r'.*?', DefaultHandler)
]
