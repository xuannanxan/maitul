# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from . import home,seo_data,cache,make_cache_key
from app.models import Crud,Category,Product
from flask import render_template, redirect, url_for,request



@home.route("/services/<int:nav_id>", methods=['GET'])
@home.route("/services", methods=['GET'])
@cache.memoize(60)
def services(nav_id=None):
    if nav_id==None:
        return redirect(url_for('home.index'))
    #如果在本页搜索
    if ('search' in request.args) and (request.args['search']):
        search = request.args['search']
        return redirect(url_for('home.products',nav_id = 53,search = search))
    products = Crud.search_data(Product,Product.relation_id == nav_id,Product.sort.desc(),9)
    return render_template(
        "home/services.html",
        seo_data = seo_data,
        products = products
    )

