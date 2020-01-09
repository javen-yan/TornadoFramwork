# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2019/12/5 上午10:41
"""
import os
from web.apps.default.controller import FileServerHandler, UploadItemHandler
from web.utils.app_route import merge_route
from web.apps.usercenter.urls import urls as users
from web.apps.taskcenter.urls import urls as tasks
from web.apps.domcenter.urls import urls as domes
from web.apps.runnercenter.urls import urls as runners
from web.apps.nodecenter.urls import urls as nodes


urlpatterns = [
    (r'/uploader$', FileServerHandler),
    (r"/uploads/(.*)", UploadItemHandler, dict(path=os.path.join(os.getcwd(), 'uploads')))
]
urlpatterns += merge_route(users, '/user-center')
urlpatterns += merge_route(tasks, '/task-center')
urlpatterns += merge_route(domes, '/dom-center')
urlpatterns += merge_route(runners, '/runner-center')
urlpatterns += merge_route(nodes, '/node-center')
