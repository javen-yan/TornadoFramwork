# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: mongoSession.py
@Software: PyCharm
@Time :    2019/12/9 下午3:04
"""
from pymongo import MongoClient
from web.settings import mg_host, mg_password, mg_port, mg_username, mg_database, mg_collection

kw = {
    "username": mg_username,
    "password": mg_password,
    "ip": mg_host,
    "port": mg_port
}

link = "mongodb://{username}:{password}@{ip}:{port}".format(**kw)
if not kw['username']:
    kw.pop('username')
    kw.pop('password')
    link = "mongodb://{ip}:{port}".format(**kw)

mgSession = MongoClient(link)
mg_default_db = mgSession.get_database(mg_database)
mg_default_collection = mg_default_db.get_collection(mg_collection)
