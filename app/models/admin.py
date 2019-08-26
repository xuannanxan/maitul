# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from werkzeug.security import check_password_hash,generate_password_hash
from  app.models.base import db,Base,login_manager
from flask_login import UserMixin
from app.models.role import Role
from app.models.log import Adminlog,Operationlog


# 管理员
class Admin(UserMixin,Base):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True,nullable=False)
    _password = db.Column('password',db.String(128),nullable=False)
    is_super = db.Column(db.SmallInteger, default=0)  # 是否超级管理员 1为是 0为否
    role_id = db.Column(db.Integer, nullable=False)  # 角色
    def __repr__(self):
        return '<Admin %r>' % self.username
    @property
    def password(self):
        """
        读取属性
        :return:
        """
        return self._password

    @password.setter
    def password(self,raw):
        """
        为password写入属性
        :param raw:明文密码
        :return:加密后的密码
        """
        self._password = generate_password_hash(raw)


    def check_pwd(self, raw):
        """
        密码验证
        :param raw:
        :return:
        """
        return check_password_hash(self._password, raw)
    # 继承了flask-login的UserMixin，主键为id，无需重新定义
    # def get_id(self):
    #     return self.id
@login_manager.user_loader
def get_admin(id):
    """
    返回用户模型
    :param id:
    :return:
    """
    return Admin.query.get(int(id))