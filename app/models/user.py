# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db,Base,login_manager
from werkzeug.security import check_password_hash,generate_password_hash
from app.expand.utils import diyId
# 会员的数据模型
class User(Base):
    __tablename__ = "user"
    id = db.Column(db.String(32), primary_key=True,default=diyId)
    email = db.Column(db.String(100), unique=True)
    _password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    info = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=1)  # 用户状态，第一位 1为已激活 0为禁用
    profile = db.Column(db.String(255))
    address = db.Column(db.String(255))


    def __repr__(self):
        return '<User %r>' % self.email
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
# @login_manager.user_loader
# def get_User(id):
#     """
#     返回用户模型
#     :param id:
#     :return:
#     """
#     return User.query.get(int(id))

