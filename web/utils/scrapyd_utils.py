# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: scrapyd_utils.py
@Software: PyCharm
@Time :    2020/1/10 上午10:54
"""
# -*- coding: utf-8 -*-

# @Date    : 2018-11-28
# @Author  : Peng Shiyu

from datetime import datetime, timedelta
from urllib.parse import urljoin
import httpx as requests
from dateutil import parser


def format_time(date_time):
    """
    格式化时间
    :param date_time: str 各种时间格式
    :return: str eg:2019-03-03 20:09:43
    """
    try:
        dt = parser.parse(date_time)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        time_str = date_time

    return time_str


def parse_time(date_time):
    try:
        dt = parser.parse(date_time)
    except TypeError:
        dt = date_time

    return dt


def format_delta(delta_time):
    if not isinstance(delta_time, timedelta):
        return ""

    delta_time = delta_time.seconds

    hour, second = divmod(delta_time, 60 * 60)
    minute, second = divmod(second, 60)

    if hour > 0:
        delta = "{}h:{}m:{}s".format(hour, minute, second)
    elif minute > 0:
        delta = "{}m:{}s".format(minute, second)
    else:
        delta = "{}s".format(second)

    return delta


def get_timestamp(end_time, start_time):
    """
    获取时间间隔的字符串格式
    """
    start_time = parse_time(start_time)
    end_time = parse_time(end_time)

    is_start_time = isinstance(start_time, datetime)
    is_end_time = isinstance(end_time, datetime)

    if all([is_start_time, is_end_time]):
        delta_time = end_time - start_time

    elif is_start_time:
        delta_time = datetime.now() - start_time
    else:
        delta_time = ""

    return format_delta(delta_time)


def get_log_url(server, project, spider, job_id):
    """
    获取日志url
    :param server: str 服务器地址
    :param project: str 项目名称
    :param spider: str 爬虫名称
    :param job_id: str 任务id
    :return: str url
    """
    # http://localserver:6801/logs/scrapy_demo/baidu/aabc0f10fb8e11e8b925f45c89bc23a1.log
    params = "logs/{}/{}/{}.log".format(project, spider, job_id)
    return urljoin(server, params)


async def get_log(url):
    """
    获取日志内容
    :param url: str
    :return:
    """
    try:
        response = await requests.get(url)
        response.encoding = response.apparent_encoding
        text = response.text
    except Exception as e:
        text = "<h2>{}</h2>".format(e)
    return "<pre>{}</pre>".format(text)


def format_version(version):
    try:
        date_time = datetime.fromtimestamp(int(version))
        version = date_time.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass
    return version


def format_time(date_time):
    """
    格式化时间
    :param   date_time: str 各种时间格式
    :return: str eg:2019-03-03 20:09:43
    """
    try:
        dt = parser.parse(date_time)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        time_str = date_time
    return time_str
