# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: middles.py
@Software: PyCharm
@Time :    2019/12/9 上午9:50
"""
from logzero import logger
from web.apps.default.globalstatus import UserCenterStatusCode
from web.apps.usercenter.libs.account import decode_jwt
from web.middles.base import Middleware
from web.utils.tools import decrypt_data


class UserAuthMiddleware(Middleware):
    """
        用户认证中间件
    """

    def process_request(self):
        logger.debug("用户认证中间件， 认证中...")
        auth_content = self.request.headers.get('Authorization', '')
        if auth_content:
            auth_prefix = 'JWT '
            if auth_content.startswith(auth_prefix):
                token = auth_content.split(" ")[1]
                res = decode_jwt(self, token)
                if res['status']:
                    self.current_user = res['data']
                else:
                    kw = {"code": res['code'], "msg": res['msg']}
                    self.set_status(403)
                    self.finish(kw)
        else:
            kw = {"code": UserCenterStatusCode.miss_token_error.value, "msg": "Token 缺失"}
            self.set_status(403)
            self.finish(kw)

    def process_response(self):
        logger.debug("用户认证中间件， 认证完成...")


class EncryptMiddleware(Middleware):
    """
        数据加密中间件
    """

    def process_request(self):
        logger.debug("加密中间件 数据过滤中...")
        self.request.body = decrypt_data(self.request.body)

    def process_response(self):
        logger.debug("加密中间件 数据过滤结束")


class AesEncryptMiddleware(Middleware):
    """
        AES数据加密中间件
    """

    def process_request(self):
        logger.debug("AES加密中间件 数据过滤中...")

    def process_response(self):
        logger.debug("AES加密中间件 数据过滤结束...")
