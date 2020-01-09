# _*_coding:utf-8_*_
"""
@ProjectName: TornadoFramwork
@Author:  Javen Yan
@File: databases.py
@Software: PyCharm
@Time :    2019/12/5 上午10:48
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from web.models.dbSession import ModelBase, dbSession
from uuid import uuid4
from datetime import datetime
from pbkdf2 import crypt


class AccountModel(ModelBase):
    __tablename__ = 'account'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    uuid = Column(String(64), default=str(uuid4()))
    username = Column(String(64), nullable=False, comment="用户登录名")
    _password = Column('password', String(64), nullable=False, comment="用户密码")
    phone = Column(String(11), comment="用户手机号")
    email = Column(String(128), comment="用户邮箱")
    avatar = Column(String(128), comment="用户头像")
    _locked = Column(Boolean, default=False, comment="锁定状态")
    _is_delete = Column(Boolean, default=False, comment="删除状态")
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='最后登录时间')

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def all(cls, DEL=False):
        return dbSession.query(cls).query_by(deleted=DEL).order_by(-cls.created_at).all()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(username=name).first()

    @staticmethod
    def _hash_password(password):
        return crypt(password, iterations=0x2537)

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    @property
    def deleted(self):
        return self._is_delete

    @deleted.setter
    def deleted(self, value):
        assert isinstance(value, bool)
        self._is_delete = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == crypt(other_password, self.password)
        else:
            return False

    @property
    def _created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def _updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'avatar': self.avatar,
            'created_at': self._created_at,
            'updated_at': self._updated_at
        }

