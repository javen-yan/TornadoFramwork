# _*_coding:utf-8_*_
"""
@ProjectName: CrawlKeeper
@Author:  Javen Yan
@File: profile.py
@Software: PyCharm
@Time :    2020/1/8 下午5:48
"""
from web.models import AccountModel
from web.apps.default.globalstatus import UserCenterStatusCode
from web.settings import sys_prefix

def get_profile(self):
    uuid = self.current_user['uuid']
    user = AccountModel.by_uuid(uuid)
    if user:
        return {'status': True, 'msg': '获取成功', 'code': UserCenterStatusCode.success.value, 'data': user.to_dict()}
    else:
        return {'status': False, 'msg': '未找到该用户', 'code': UserCenterStatusCode.account_error.value}


def modify_profile(self, email, phone, old_password, new_password, avatar):
    uuid = self.current_user['uuid']
    user = AccountModel.by_uuid(uuid)
    if user:
        if phone:
            user.phone = phone
        if email:
            user.email = email
        if avatar:
            user.avatar = sys_prefix + '/' + avatar if sys_prefix else ''
        if old_password and not new_password:
            return {'status': False, 'msg': '新密码不能为空', 'code': UserCenterStatusCode.password_error.value}
        elif not old_password and new_password:
            return {'status': False, 'msg': '请输入旧密码', 'code': UserCenterStatusCode.password_error.value}
        elif new_password and old_password:
            if user.auth_password(old_password):
                user.password = new_password
            else:
                return {'status': False, 'msg': '旧密码不正确', 'code': UserCenterStatusCode.password_error.value}
        self.db.add(user)
        self.db.commit()
        return {'status': True, 'msg': '信息更新成功', 'code': UserCenterStatusCode.success.value}
    else:
        return {'status': False, 'msg': '未找到该用户', 'code': UserCenterStatusCode.account_error.value}