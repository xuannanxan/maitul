# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from flask import render_template

from app.models import Crud,Product,Category
from . import home,seo_data,cache


@home.route("/")
@cache.cached(key_prefix='index')#设置一个key_prefix来作为标记,调用cache.delete('index')来删除缓存来保证用户访问到的内容是最新的
def index():
    nav_id = 53
    products_column = Crud.search_data(Category,Category.pid == nav_id)
    products_column_ids = [v.id for v in products_column]
    products_column_ids.append(nav_id)
    products = Crud.search_data_paginate(Product,Product.column_id.in_(products_column_ids),Product.sort.desc(),number=8)
    request_data = {}
    return render_template("home/index.html",
                           products = products,
                           request_data = request_data,
                           seo_data =seo_data
                           )

