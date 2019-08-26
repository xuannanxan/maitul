# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db,Base

# 菜单
class Menu(Base):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    icon = db.Column(db.String(100))
    url = db.Column(db.String(255))
    pid = db.Column(db.Integer)  # 上级菜单
    sort = db.Column(db.Integer, default=0)  # 排序

    def __repr__(self):
        return '<Menu %r>' % self.name