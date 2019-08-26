# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base


# 用户足迹

class Footmark(Base):
    __tablename__ = "footmark"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # IP地址
    uid = db.Column(db.String(255))  # 用户
    url = db.Column(db.String(255))  # 查看的页面
    content = db.Column(db.String(255))  # 查看内容
    def __repr__(self):
        return '<Footmark %r>' % self.id

