# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base


# 爬虫请求页面
class ReptileRequest(Base):
    __tablename__ = "reptile_request"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    begin_page = db.Column(db.String(20))
    end_page = db.Column(db.String(20))
    dom = db.Column(db.String(255), nullable=False)  # 页面的dom
    content_name = db.Column(db.String(255), nullable=False)  # 内容元素定位
    content_info = db.Column(db.String(255))  # 内容元素定位
    content_main = db.Column(db.String(255), nullable=False)  # 内容元素定位
    content_img = db.Column(db.String(255))  # 内容元素定位
    def __repr__(self):
        return '<ReptileRequest %r>' % self.name
# 爬取的列表页面
class ReptileList(Base):
    __tablename__ = "reptile_list"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    content_name = db.Column(db.String(255))  # 内容元素定位
    content_info = db.Column(db.Text())  # 内容元素定位
    content_main = db.Column(db.Text())  # 内容元素定位
    content_img = db.Column(db.Text())  # 内容元素定位

    def __repr__(self):
        return '<ReptileList %r>' % self.content_name
