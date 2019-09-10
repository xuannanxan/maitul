# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base


# 页面设置，设置模板等信息
class Template(Base):
    __tablename__ = "template"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    nav_id = db.Column(db.Integer)  # 导航0为首页
    template = db.Column(db.String(255)) # 模板页面，如product.html,index.html
    bgcolor = db.Column(db.String(255)) # 背景颜色，默认为白色
    data_type = db.Column(db.SmallInteger, default=1) # 数据类型，1栏目数据，2广告数据
    data_id = db.Column(db.Integer)  # 数据id，栏目数据就选择栏目，广告数据就选择广告位
    data_num = db.Column(db.Integer)  # 数据数量，如果分页就是每页数量
    pagination = db.Column(db.SmallInteger, default=0) # 是否分页，0不分页，1分页
    show_title = db.Column(db.SmallInteger, default=0) # 是否显示标题，0不显示，1显示
    sort = db.Column(db.Integer, default=0)  # 排序
    
    def __repr__(self):
        return '<Tag %r>' % self.name