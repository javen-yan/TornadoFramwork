# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/1/7 下午4:28
"""
from web.apps.nodecenter.controller import NodesHandler, NodesStatusHandler, NodeProjectHandler, \
    NodeProjectSpiderHandler, NodeProjectJobsHandler

urls = [
    (r'', NodesHandler),
    (r'/status', NodesStatusHandler),
    (r'/projects', NodeProjectHandler),
    (r'/spiders', NodeProjectSpiderHandler),
    (r'/jobs', NodeProjectJobsHandler),
]