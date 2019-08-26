# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db,Base


# 角色
class Role(Base):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True,nullable=False)
    auths = db.Column(db.String(512))
  

    def __repr__(self):
        return '<Role %r>' % self.name

# 权限
class Auth(Base):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(255))
    menu_id = db.Column(db.Integer)  # 所属菜单

    def __repr__(self):
        return '<Auth %r>' % self.name