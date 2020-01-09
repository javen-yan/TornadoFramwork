# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: nodes.py
@Software: PyCharm
@Time :    2020/1/9 下午5:23
"""
from logzero import logger

from web.apps.default.thirdapi.scrapyd_api import ScarpedApi
from web.models.databases import NodeServerModel
from web.apps.default.globalstatus import StatusCode


async def add_node_server(self, name, url):
    if not name:
        return {"status": False, "msg": "服务名必须存在", "code": StatusCode.miss_params_error.value}
    if not url:
        return {"status": False, "msg": "服务地址必须存在", "code": StatusCode.miss_params_error.value}
    if NodeServerModel.by_url(url.strip()):
        return {"status": False, "msg": "服务地址已存在", "code": StatusCode.exist_error.value}
    if NodeServerModel.by_name(name.strip()):
        return {"status": False, "msg": "服务名已存在", "code": StatusCode.exist_error.value}
    try:
        node = NodeServerModel()
        node.server_name = name
        node.server_url = url
        self.db.add(node)
        self.db.commit()
        return {"status": True, "msg": "添加成功", "code": StatusCode.success.value}
    except Exception as e:
        logger.exception(e)
        self.db.rollback()
        return {"status": False, "msg": "数据库操作失败", "code": StatusCode.db_error.value}


async def delete_server(self, uuid):
    row = NodeServerModel.by_uuid(uuid)
    if row:
        try:
            self.db.delete(row)
            self.db.commit()
            return {"status": True, "msg": "删除成功", "code": StatusCode.success.value}
        except Exception as e:
            logger.exception(e)
            self.db.rollback()
            return {"status": False, "msg": "数据库操作失败", "code": StatusCode.db_error.value}
    else:
        return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}


async def get_servers(self, uuid=None):
    if uuid:
        row = NodeServerModel.by_uuid(uuid)
        if row:
            server = row.to_dict()
            api = ScarpedApi(**{"node_url": server.get('server_url')})
            status = await api.get_status()
            server['server_status'] = status
            return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': server}
        else:
            return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
    else:
        result = list()
        rows = NodeServerModel.all()
        for row in rows:
            server = row.to_dict()
            api = ScarpedApi(**{"node_url": server.get('server_url')})
            status = await api.get_status()
            server['server_status'] = status
            result.append(server)
        return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': result}