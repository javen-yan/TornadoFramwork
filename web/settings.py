# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: settings.py
@Software: PyCharm
@Time :    2019/12/5 上午10:23
"""
import configparser
conf = configparser.ConfigParser()
conf.read('config.ini')


def get_config(namespace, key, default=None):
    result = default
    try:
        namespace = conf[namespace]
        if namespace:
            result = namespace[key]
    except Exception as e:
        print(f"ConfigParser Key Error: {e}")
        result = default
    return result


def split_value(data):
    result = []
    for d in data.split(','):
        if not d:
            continue
        else:
            result.append(d)
    return result


JWT_EXPIRE_LIST = [int(i) for i in get_config(
    'system', 'jwt_expire').split("*")]  # jwt 过期时间

# 系统配置映射
sys_debug = get_config('system', 'debug')
sys_secret = get_config('system', 'secret')
sys_login_url = get_config('system', 'login_url')
sys_static = get_config('system', 'static')
sys_templates = get_config('system', 'templates')
sys_static_url_prefix = get_config('system', 'static_url_prefix')
sys_xsrf_cookies = get_config('system', 'xsrf_cookies')
sys_port = int(get_config('system', 'port'))
sys_auto_reload = get_config('system', 'auto_reload')
sys_jwt_expire = JWT_EXPIRE_LIST[0] * JWT_EXPIRE_LIST[1] * JWT_EXPIRE_LIST[2]
sys_public_key = get_config('system', 'public_key')
sys_private_key = get_config('system', 'private_key')
sys_aes_key = get_config('system', 'aes_key')
sys_aes_iv = get_config('system', 'aes_iv')


# 数据库配置映射
db_username = get_config('database', 'USERNAME')
db_port = int(get_config('database', 'port'))
db_database = get_config('database', 'DATABASE')
db_hostname = get_config('database', 'HOSTNAME')
db_password = get_config('database', 'PASSWORD')

# 中间件
md = get_config('middleware', 'middleware_list')
middleware_list = split_value(md)

# mongo db 配置映射
mg_host = get_config('mongo', 'host')
mg_port = int(get_config('mongo', 'port'))
mg_username = get_config('mongo', 'username')
mg_password = get_config('mongo', 'password')
mg_database = get_config('mongo', 'database')
mg_collection = get_config('mongo', 'collection')
