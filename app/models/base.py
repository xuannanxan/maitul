# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
import traceback
from copy import deepcopy
from flask import current_app
from app.expand.utils import object_to_dict
from app.extensions import db,login_manager
from datetime import datetime
from sqlalchemy.sql import and_,or_,not_
db = db
and_ = and_
or_ = or_
not_ = not_
login_manager = login_manager


class Base(db.Model):
    #不需要创建base表
    __abstract__ = True
    #所有模型继承的字段
    create_time = db.Column(db.DateTime, nullable=True,default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    is_del = db.Column(db.Integer, default=0)  # 状态，0为未删除，其他为已删除
    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key != "id":
                setattr(self,key,value)
        # setattr(self,'create_time',datetime.now)

class Crud:
    def auto_commit(sql):
        """
        提交sql语句
        :sql :
        :return: 提示信息
        """
        try:
            data = db.session.execute(sql)
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False
    def easy_add(data):
        try:
            db.session.add(data)
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False

    def add_all(data):
        try:
            db.session.add_all(data)
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False

    def add(model,data,not_repeat = None):
        """
        添加
        :param :
        :return: 提示信息
        """
        try:
            if not_repeat != None:
                count = model.query.filter(model.is_del == 0,getattr(model, not_repeat)==data[not_repeat]).count()
                if count > 0:
                    return  False
            model_data = model()
            model_data.set_attrs(data)
            db.session.add(model_data)
            db.session.commit()
            return model_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False

    def get_data_paginate(model, sort="id", page=None, number=10):
        """
        获取列表信息，带分页
        :param sort: 排序字段
        :param page: 页面
        :param number: 每页数量
        :return:带分页的数据
        """
        if page is None:
            page = 1
        page_data = model.query.filter(
            model.is_del == 0
        ).order_by(
                sort
        ).paginate(page, per_page=number)
        return page_data

    def get_data(model, sort="id"):
        """
        获取不带分页的数据
        :param sort: 排序字段
        :return: 不分页的全部数据
        """
        data = model.query.filter(model.is_del == 0).order_by(sort).all()
        return data

    def get_data_by_id(model, id):
        """
        按ID获取数据
        :param id:
        :return:
        """
        data = model.query.get_or_404(id)
        return data

    def search_data(model, queries=[], sort="id",number=0):
        """

        :param queries:
        :return:
        """
        param = []
        if not isinstance(queries,list):
            #如果不是数组输入，就转为数组
            param.append(queries)
        else:
            param = queries
        param.append(model.is_del == 0)
        if number > 0:
            return  model.query.filter(*param).order_by(sort).limit(number).all()
        else:
            return model.query.filter(*param).order_by(sort).all()

    def search_data_paginate(model, queries=[], sort="id",page=None, number=10):
        """

        :param queries:
        :return:
        """
        param = []
        if not isinstance(queries,list):
            #如果不是数组输入，就转为数组
            param.append(queries)
        else:
            param = queries
        param.append(model.is_del == 0)
        data = model.query.filter(*param).order_by(sort).paginate(page, per_page=number)
        return data


    def update(model,data,not_repeat = None):
        """
        更新
        :param :
        :return: 提示信息
        """
        try:
            model_data = Crud.get_data_by_id(model, data["id"])
            copy_data = deepcopy(model_data)
            if not_repeat != None:
                count = model.query.filter(model.is_del == 0,getattr(model, not_repeat)==data[not_repeat]).count()
                if count == 1 and object_to_dict(copy_data)[not_repeat] != data[not_repeat]:
                    return  False
            model_data.set_attrs(data)
            db.session.commit()
            return model_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False

    def easy_update(data):
        try:
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False

    def delete(data):
        """
        删除
        :param id:
        :return: 提示信息
        """
        try:
            data.is_del = data.id
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False


    def clean(data):
        # 彻底删除
        try:
            db.session.delete(data)
            # 提交数据库会话
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False

    def clean_all(lst):
        # 彻底删除多行
        try:
            if type(lst).__name__ == 'list' :
                for v in lst:
                    db.session.delete(v)
                db.session.commit()
                return len(lst)
            return False
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(e)
            return False