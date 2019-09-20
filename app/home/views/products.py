# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from . import home,seoData,cache,make_cache_key,CLICKS_COUNT
from app.models import Crud,Category,Product,Tag,TagRelation
from flask import render_template, redirect, url_for,flash,session,request,g
from sqlalchemy import or_,and_
from app.expand.utils import object_to_dict


@home.route("/products1/<int:nav_id>", methods=['GET'])
@home.route("/products1", methods=['GET'])
@cache.cached(timeout=60, key_prefix=make_cache_key)
def products(nav_id=None):
    if nav_id==None:
        return redirect(url_for('home.index'))
    #参数转为字典
    request_data = request.args.to_dict()
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1
    param = []
    #栏目筛选，当前栏目的所有子栏目
    products_column = Crud.search_data(Category,Category.pid == nav_id)
    products_column_ids = [v.id for v in products_column]
    products_column_ids.append(nav_id)
    param.append(Product.column_id.in_(products_column_ids))
    # 根据关联栏目筛选
    if ('services' in request.args) and (request.args['services']):
        services = request.args['services']
        param.append(Product.relation_id==services)
    #根据搜索条件筛选
    if ('search' in request.args) and (request.args['search']):
        search = request.args['search']
        param.append(or_(Product.title.like("%" + search + "%"),Product.info.like("%" + search + "%"),Product.content.like("%" + search + "%")))
    #根据标签筛选
    if ('tag' in request.args) and (request.args['tag']):
        tag = request.args['tag']
        param.append(product_tag.c.tag_id == tag)
        param.append(Product.is_del == 0)
        products = Product.query.join(product_tag).filter(*param).order_by(Product.sort.desc()).paginate(page, 8)
    #如果没有标签信息，就不需要连表查询
    else:
        products = Crud.search_data_paginate(Product,param,Product.sort.desc(),page,8)
    return render_template(
        "home/products.html",
        request_data = request_data,
        seo_data = seo_data,
        products = products
    )
#产品详情
@home.route("/product/<int:nav_id>/<int:id>", methods=['GET'])
@cache.memoize(60)
def product(nav_id=None,id=None):
    rule = str(request.path)
    if id==None or nav_id==None:
        return redirect(url_for('home.index'))
    #如果在详情页搜索
    if ('search' in request.args) and (request.args['search']):
        search = request.args['search']
        return redirect(url_for('home.products',nav_id = nav_id,search = search))
    #获取产品的详细信息
    product_detail = Crud.get_data_by_id(Product,id)
    #如果点击量为None，赋值0
    if not product_detail.click:
            product_detail.click = 0
    #如果有缓存的点击量，更新点击量
    if rule in CLICKS_COUNT:
        product_detail.click = int(product_detail.click) + int(CLICKS_COUNT[rule])
    else:
        product_detail.click = int(product_detail.click)+1
    Crud.easy_update(product_detail)
    # 如果进行了非法操作
    if product_detail.column_id != nav_id:
         return redirect(url_for('home.index'))
     #获取相识产品，用途和分类一致的产品
    similar_products = Crud.search_data(Product,and_(Product.column_id == product_detail.column_id,Product.relation_id == product_detail.relation_id),Product.sort.desc(),9)
    #获取标签作为关键词
    keywords = ','.join([v.name for v in product_detail.tags])
    #获取图集
    pictures = product_detail.pictures.split(',')
    product_data = object_to_dict(product_detail)
    product_data['pictures'] = pictures
    #SEO信息
    seo_data.keywords =  keywords
    seo_data.description = product_detail.description
    seo_data.title = product_detail.title
    return render_template(
        "home/product.html",
        product_data=product_data,
        seo_data = seo_data,
        similar_products = similar_products
        )
