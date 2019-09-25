# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base


# 标签
class Tag(Base):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sort = db.Column(db.Integer, default=0)  # 排序

    def __repr__(self):
        return '<Tag %r>' % self.name

# 关联的标签
class TagRelation(Base):
    __tablename__ = "tag_relation"
    tag_type = db.Column(db.SmallInteger, primary_key=True)  # 标签类型，1为产品，2为文章,''为其他
    relation_id = db.Column(db.String(32), primary_key=True)  # 关联id
    tag_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<TagRelation %r>' % self.relation_id