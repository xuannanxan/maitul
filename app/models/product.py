# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base
from app.expand.utils import diyId



# 内容
class Product(Base):
    __tablename__ = "product"
    id = db.Column(db.String(32), primary_key=True,default=diyId)
    title = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(255))
    pictures = db.Column(db.Text)
    price = db.Column(db.Float,default=0)
    keywords = db.Column(db.String(200))
    description = db.Column(db.String(255))# 用于seo的描述信息
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    click = db.Column(db.BigInteger,default=0)  # 点击数
    sort = db.Column(db.Integer, default=1)  # 排序
    admin_id = db.Column(db.String(255))  # 发布用户
    relation_id = db.Column(db.Integer)  # 关联id
    category_id = db.Column(db.Integer)  # 所属栏目

    def __repr__(self):
        return '<Product %r>' % self.title




