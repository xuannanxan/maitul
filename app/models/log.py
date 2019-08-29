# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db,Base

# 管理员登录日志
class Adminlog(Base):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    ip = db.Column(db.String(100))
    info = db.Column(db.String(255))

    def __repr__(self):
        return '<Adminlog %r>' % self.id


# 管理员操作日志
class Operationlog(Base):
    __tablename__ = "operationlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))  # 操作原因

    def __repr__(self):
        return '<Operationlog %r>' % self.id

# 会员登录日志
class Userlog(Base):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ip = db.Column(db.String(100))

    def __repr__(self):
        return '<Userlog %r>' % self.id
