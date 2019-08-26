# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db,Base

# 广告
class Ad(Base):
    __tablename__ = "ad"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    info = db.Column(db.Text)
    url = db.Column(db.String(255))
    img = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)  # 排序
    space_id = db.Column(db.Integer)  # 关联广告位

    def __repr__(self):
        return '<Ad %r>' % self.title


# 广告位
class Adspace(Base):
    __tablename__ = "adspace"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    ename = db.Column(db.String(100))
   

    def __repr__(self):
        return '<Adspace %r>' % self.name