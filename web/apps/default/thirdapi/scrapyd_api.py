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
        result = await requests.get(url=self.node.get('node_url') + '/daemonstatus.json')
        try:
            response = result.json()
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
        result = await requests.post(url=self.node.get('node_url') + '/addversion.json', files=files)
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
        result = await requests.post(url=self.node.get('node_url') + '/schedule.json', data=data)
        try:
            response = result.json()
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
        result = await requests.post(url=self.node.get('node_url') + '/cancel.json', data=data)
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_projects(self):
        """获取所有项目"""
        response = None
        result = await requests.get(url=self.node.get('node_url') + '/listprojects.json')
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_project_version(self, project):
        """获取所有项目"""
        response = None
        result = await requests.get(url=self.node.get('node_url') + '/listversions.json', params={"project": project})
        try:
            response = result.json()
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
        result = await requests.get(url=self.node.get('node_url') + '/listversions.json', params=params)
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def get_project_jobs(self, project):
        """获取项目任务"""
        response = None
        result = await requests.get(url=self.node.get('node_url') + '/listjobs.json', params={"project": project})
        try:
            response = result.json()
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
        result = await requests.post(url=self.node.get('node_url') + '/delversion.json', data=data)
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response

    async def del_project(self, project):
        """删除项目"""
        response = None
        data = {
            "project": project
        }
        result = await requests.post(url=self.node.get('node_url') + '/delproject.json', data=data)
        try:
            response = result.json()
        except Exception as e:
            logger.error(f"ScarpedApi -> Error: {e} | Response: {result.text}")
        return response
