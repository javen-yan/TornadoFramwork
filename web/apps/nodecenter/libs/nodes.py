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
from web.utils import scrapyd_utils
from web.utils.date2json import to_json


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


async def get_server_status(self, uuid=None):
    if uuid:
        row = NodeServerModel.by_uuid(uuid)
        if row:
            server = row.to_dict()
            api = ScarpedApi(**server)
            status = await api.get_status()
            if status:
                server.update(status)
            return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': server}
        else:
            return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
    else:
        result = list()
        rows = NodeServerModel.all()
        for row in rows:
            server = row.to_dict()
            api = ScarpedApi(**server)
            status = await api.get_status()
            if status:
                server['server_status'] = status
            result.append(server)
        return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': result}


async def get_servers(self, uuid=None):
    if uuid:
        row = NodeServerModel.by_uuid(uuid)
        if row:
            server = row.to_dict()
            return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': server}
        else:
            return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
    else:
        rows = NodeServerModel.all()
        return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': to_json(rows)}


async def get_node_projects(self, uuid):
    if uuid:
        row = NodeServerModel.by_uuid(uuid)
        if row:
            server = row.to_dict()
            api = ScarpedApi(**server)
            projects = await api.get_projects()
            if projects:
                lst = []
                for project in projects:
                    versions = await api.get_project_version(project)
                    if versions:
                        for version in versions:
                            item = {
                                "project_name": project,
                                "human_version": scrapyd_utils.format_version(version),
                                "version": version
                            }
                            lst.append(item)
                server['projects'] = lst
                return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value,
                        'data': server}
            else:
                return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value, 'data': server}
        else:
            return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
    else:
        return {"status": False, "msg": "UUID不能为空", "code": StatusCode.miss_params_error.value}


async def get_node_project_spiders(self, uuid, project):
    if not project:
        return {"status": False, "msg": "项目名称不能为空", "code": StatusCode.miss_params_error.value}
    if uuid:
        row = NodeServerModel.by_uuid(uuid)
        if row:
            server = row.to_dict()
            server['project_name'] = project
            api = ScarpedApi(**server)
            spiders = await api.get_project_spiders(project)
            if spiders:
                server['spiders'] = [{"spider_name": spider} for spider in spiders]
                return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value,
                        'data': server}
            else:
                return {"status": True, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
        else:
            return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
    else:
        return {"status": False, "msg": "UUID不能为空", "code": StatusCode.miss_params_error.value}


async def get_node_project_jobs(self, uuid, project):
    if not project:
        return {"status": False, "msg": "项目名称不能为空", "code": StatusCode.miss_params_error.value}
    if uuid:
        row = NodeServerModel.by_uuid(uuid)
        if row:
            server = row.to_dict()
            server['project_name'] = project
            api = ScarpedApi(**server)
            jobs = await api.get_project_jobs(project)
            lst = []
            if jobs:
                for job_status, job_list in jobs.items():
                    for job in job_list:
                        item = {
                            "status": job_status,
                            "spider": job["spider"],
                            "start_time": scrapyd_utils.format_time(job.get("start_time", "")),
                            "end_time": scrapyd_utils.format_time(job.get("end_time", "")),
                            "timestamp": scrapyd_utils.get_timestamp(job.get("end_time"), job.get("start_time")),
                            "job_id": job["id"]
                        }
                        lst.append(item)
                server['jobs'] = lst
                return {"status": True, "msg": "数据获取成功", "code": StatusCode.success.value,
                        'data': server}
            else:
                return {"status": True, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
        else:
            return {"status": False, "msg": "未找到相关数据", "code": StatusCode.not_found_error.value}
    else:
        return {"status": False, "msg": "UUID不能为空", "code": StatusCode.miss_params_error.value}