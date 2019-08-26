# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models.base import db, Base


# 配置项
class Conf(Base):
    __tablename__ = "conf"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.SmallInteger, default=1)  # 配置类型，1为文本，2为数字,3为文本域，4为下拉单选，5为下拉多选，6为图片，7为富文本
    placeholder = db.Column(db.String(100))
    optional_values = db.Column(db.Text) #可选值
    default_value = db.Column(db.Text)
    sort = db.Column(db.Integer, default=0)  # 排序

    def __repr__(self):
        return '<Conf %r>' % self.name
