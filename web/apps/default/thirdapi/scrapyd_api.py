# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: scrapyd_api.py
@Software: PyCharm
@Time :    2020/1/9 下午2:56
"""
import httpx as requests
from logzero import logger


class ScarpedApi(object):

    def __init__(self, **kwargs):
        self.node = kwargs

    async def get_status(self):
        """获取当前节点可用资源"""
        response = None
        result = await requests.get(url=self.node.get('server_url') + '/daemonstatus.json')
        try:
            response = result.json()
            response.pop('node_name')
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def add_version(self, project, version, egg_file):
        """获取增加项目运行新版本"""
        response = None
        files = {
            "project": project,
            "version": version,
            "egg": egg_file
        }
        result = await requests.post(url=self.node.get('server_url') + '/addversion.json', files=files)
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def add_schedule_job(self, project, spider, setting=None, job_id=None, version=None):
        """获取增加执行job"""
        response = None
        data = {
            "project": project,
            "spider": spider
        }
        if setting:
            data['setting'] = setting
        if job_id:
            data['jobid'] = job_id
        if version:
            data['_version'] = version
        result = await requests.post(url=self.node.get('server_url') + '/schedule.json', data=data)
        try:
            response = result.json().get('jobid')
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def cancel_job(self, project, job):
        """取消执行job"""
        response = None
        data = {
            "project": project,
            "job": job
        }
        result = await requests.post(url=self.node.get('server_url') + '/cancel.json', data=data)
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_projects(self):
        """获取所有项目"""
        response = None
        result = await requests.get(url=self.node.get('server_url') + '/listprojects.json')
        try:
            response = result.json().get('projects', [])
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_project_version(self, project):
        """获取所有项目"""
        response = None
        result = await requests.get(url=self.node.get('server_url') + '/listversions.json', params={"project": project})
        try:
            response = result.json().get('versions', [])
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_project_spiders(self, project, version=None):
        """获取所有项目"""
        response = None
        params = {
            "project": project
        }
        if version:
            params["_version"] = version
        result = await requests.get(url=self.node.get('server_url') + '/listspiders.json', params=params)
        try:
            response = result.json().get('spiders', [])
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_project_jobs(self, project):
        """获取项目任务"""
        response = None
        result = await requests.get(url=self.node.get('server_url') + '/listjobs.json', params={"project": project})
        try:
            jobs = result.json()
            response = {
                "pending": jobs.get("pending", []),
                "running": jobs.get("running", []),
                "finished": jobs.get("finished", [])
            }
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def del_version(self, project, version):
        """删除项目版本"""
        response = None
        data = {
            "project": project,
            "version": version
        }
        result = await requests.post(url=self.node.get('server_url') + '/delversion.json', data=data)
        try:
            response = result.json().get('status') == 'ok'
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def del_project(self, project):
        """删除项目"""
        response = None
        data = {
            "project": project
        }
        result = await requests.post(url=self.node.get('server_url') + '/delproject.json', data=data)
        try:
            response = result.json().get('status') == 'ok'
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    server = {"server_url": "http://127.0.0.1:6800"}
    api = ScarpedApi(**server)
    # row = loop.run_until_complete(api.get_projects())
    # row2 = loop.run_until_complete(api.get_project_version('baidu'))
    # row3 = loop.run_until_complete(api.get_project_jobs('baidu'))
    # row4 = loop.run_until_complete(api.get_project_spiders('baidu'))
    row5 = loop.run_until_complete(api.add_schedule_job('baidu', 'demo'))
    # print(row)
    # print(row2)
    # print(row3)
    # print(row4)
    print(row5)