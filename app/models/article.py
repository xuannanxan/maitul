# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db,Base

# 内容
class Article(Base):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    keywords = db.Column(db.String(200))
    description = db.Column(db.String(255))# 用于seo的描述信息
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    cover = db.Column(db.String(255))
    click = db.Column(db.BigInteger)  # 点击数
    sort = db.Column(db.Integer, default=0)  # 排序
    admin_id = db.Column(db.String(255))  # 发布用户
    relation_id = db.Column(db.Integer)  # 关联id
    category_id = db.Column(db.Integer)  # 所属栏目

    def __repr__(self):
        return '<Article %r>' % self.title



