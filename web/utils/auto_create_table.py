# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: auto_create_table.py
@Software: PyCharm
@Time :    2019/12/9 下午4:17
"""
import pymysql
from web.settings import db_port, db_hostname, db_password, db_username, db_database


def get_create_sql(**kwargs):
    insert_sql_header = "CREATE TABLE `{}` (" .format(
        kwargs.get('request_name'))
    insert_sql_end = ")"
    insert_sql_body = "`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    if isinstance(kwargs.get('args'), list):
        for i in kwargs.get('args'):
            if i == 'id':
                continue
            insert_sql_body += "`{}` varchar(128),".format(i)

    return insert_sql_header + insert_sql_body[:-1] + insert_sql_end


def create_table(**kwargs):
    conn = pymysql.connect(host=db_hostname, port=db_port,
                           user=db_username, password=db_password, database=db_database)
    cursor = conn.cursor()
    sql = get_create_sql(**kwargs)
    try:
        cursor.execute(sql)
        conn.commit()
        return True, '创建{}表成功'.format(kwargs.get('request_name'))
    except Exception as e:
        conn.rollback()
        return False, '创建{}表失败: 错误: {}'.format(kwargs.get('request_name'), e)


def get_tables():
    conn = pymysql.connect(host=db_hostname, port=db_port,
                           user=db_username, password=db_password, database=db_database)
    cursor = conn.cursor()
    sql = "show tables;"
    cursor.execute(sql)
    tables = cursor.fetchall()
    result = []
    for table in tables:
        result.append(table[0])
    return result


def get_scheme(table):
    conn = pymysql.connect(host=db_hostname, port=db_port,
                           user=db_username, password=db_password, database=db_database)
    cursor = conn.cursor()
    sql = "select COLUMN_NAME from information_schema.COLUMNS" \
          " where table_name = '{}' and table_schema = '{}';".format(
              table, db_database)
    cursor.execute(sql)
    schemes = cursor.fetchall()
    result = []
    for table in schemes:
        result.append(table[0])
    return result
