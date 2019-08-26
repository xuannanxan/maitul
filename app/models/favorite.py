# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-08-24.
__author__ = 'Allen xu'
from  app.models.base import db, Base
# 收藏
class Favorite(Base):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    favorite_type = db.Column(db.SmallInteger)  # 留言类型，1为产品咨询，2为文章互动,''为其他
    relation_id = db.Column(db.Integer)  # 关联id
    uid = db.Column(db.String(255))  # 收藏用户

    def __repr__(self):
        return '<Favorite %r>' % self.id