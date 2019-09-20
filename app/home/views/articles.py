# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from . import home,seoData,cache,make_cache_key,CLICKS_COUNT
from app.models import Crud,Category,Article,Tag,Admin
from  app.models.base import db
from flask import render_template, redirect, url_for,flash,session,request
from sqlalchemy import or_,and_
import logging



@home.route("/articles/<int:nav_id>", methods=['GET'])
@home.route("/articles", methods=['GET'])
@cache.cached(timeout=60, key_prefix=make_cache_key)
def articles(nav_id=None):
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
    articles_column = Crud.search_data(Category,Category.pid == nav_id)
    articles_column_ids = [v.id for v in articles_column]
    articles_column_ids.append(nav_id)
    param.append(Article.column_id.in_(articles_column_ids))

    #根据搜索条件筛选
    if ('search' in request.args) and (request.args['search']):
        search = request.args['search']
        param.append(or_(Article.title.like("%" + search + "%"),Article.info.like("%" + search + "%"),Article.content.like("%" + search + "%")))
    #根据标签筛选
    if ('tag' in request.args) and (request.args['tag']):
        tag = request.args['tag']
        param.append(article_tag.c.tag_id == tag)
        param.append(Article.is_del == 0)
        articles = Article.query.join(article_tag).filter(*param).order_by(Article.sort.desc()).paginate(page,4)
    else:
        articles = Crud.search_data_paginate(Article,param,Article.sort.desc(),page,4)
        #articles = db.session.query(Article,Admin).join(Admin,Article.admin_id == Admin.id).filter(*param).order_by(Article.sort.desc()).paginate(page,4)
    return render_template(
        "home/articles.html",
        request_data = request_data,
        seo_data = seo_data,
        articles = articles
    )
#文章详情
@home.route("/article/<int:nav_id>/<int:id>", methods=['GET'])
@cache.memoize(60)
def article(nav_id=None,id=None):
    rule = str(request.path)
    if id==None or nav_id==None:
        return redirect(url_for('home.index'))
    #如果在详情页搜索
    if ('search' in request.args) and (request.args['search']):
        search = request.args['search']
        return redirect(url_for('home.articles',nav_id = nav_id,search = search))
    #获取产品的详细信息
    article_detail = Crud.get_data_by_id(Article,id)
    #如果点击量为None，赋值0
    if not article_detail.click:
            article_detail.click = 0
    #如果有缓存的点击量，更新点击量
    if rule in CLICKS_COUNT:
        article_detail.click = int(article_detail.click) + int(CLICKS_COUNT[rule])
    else:
        article_detail.click = int(article_detail.click)+1
    Crud.easy_update(article_detail)
    # 如果进行了非法操作
    if article_detail.column_id != nav_id:
         return redirect(url_for('home.index'))
    #获取标签作为关键词
    keywords = ','.join([v.name for v in article_detail.tags])

    #SEO信息
    seo_data.keywords =  keywords
    seo_data.description = article_detail.description
    seo_data.title = article_detail.title
    return render_template(
        "home/article.html",
        article_data=article_detail,
        seo_data = seo_data,
        )
