# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'

from  app.models.base import db,Base
# 栏目
class Category(Base):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SmallInteger, default=1)  # 栏目类型，1为产品，2为文章,3为外链
    icon = db.Column(db.String(100))
    name = db.Column(db.String(200),nullable=False)
    keywords = db.Column(db.String(200))
    info = db.Column(db.Text)
    ename = db.Column(db.String(200))# 栏目的调用名称
    content = db.Column(db.Text)# 栏目内容
    is_nav = db.Column(db.SmallInteger, default=1)# 是否导航，1为是，0为否，默认1
    cover = db.Column(db.String(255))
    url = db.Column(db.String(255))
    pid = db.Column(db.Integer, default=0)  # 上级栏目
    sort = db.Column(db.Integer, default=0)  # 排序
   

    def __repr__(self):
        return '<Category %r>' % self.name