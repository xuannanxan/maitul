# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base


# 页面设置，设置模板等信息
class PageSetup(Base):
    __tablename__ = "page_setup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    category_id = db.Column(db.Integer)  # 所属栏目
    template = db.Column(db.String(255)) # 模板名称，如product.html,index.html
    data_type = db.Column(db.SmallInteger, default=1) # 数据类型，1栏目数据，2广告数据
    data_id = db.Column(db.Integer)  # 数据id
    data_num = db.Column(db.Integer)  # 数据数量
    sort = db.Column(db.Integer, default=0)  # 排序
    
    def __repr__(self):
        return '<Tag %r>' % self.name