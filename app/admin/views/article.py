# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import ArticleForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict,build_tree
from app.models import Article,Crud,Category,Tag,TagRelation,and_
from .. import admin


# 添加文章
@admin.route("/article/add", methods=['POST'])
@login_required
@auth_required
def article_add():
    data = request.form
    form = ArticleForm(data)
    if form.validate():
        # 先添加产品信息  
        article_data = Crud.add(Article,data)
        if article_data:
            # 如果有标签信息，根据产品的id和标签ID保存关联的标签数据
            if data['tags']:
                tags = data['tags'].split(',') 
                tag_data = [TagRelation(
                    tag_type = 2,
                    relation_id = article_data.id,
                    tag_id =v
                ) for v in tags]
                Crud.add_all(tag_data)
            op_log("添加文章-%s" % article_data.title)
            return {"code": 1, "msg": "添加成功"}
        return {"code": 0, "msg": '添加失败，系统错误'}
    return {"code": 0, "msg": form.get_errors()}


# 文章列表
@admin.route("/article/list", methods=['GET'])
@login_required
@auth_required
def article_list():
    category_id = None
    page = 1
    search = ''
    if request.args.get('category_id'):
        category_id = int(request.args.get('category_id'))
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('search'):
        search = request.args.get('search')
    #产品可用标签
    tag_data = Crud.get_data(Tag)
    #栏目树
    category_data = Crud.get_data(Category, Category.sort.desc())
    category_tree = build_tree(category_data, 0, 0)
    #产品栏目
    article_category = [v  for v in category_tree if v['type'] == 2 or v['type'] == 3 ]
    if category_id == None:
        article_data = Crud.search_data_paginate(Article,Article.title.like("%" + search + "%"),Article.sort.desc(),page,10)
    else:
        article_data = Crud.search_data_paginate(Article,and_(Article.category_id == category_id,Article.title.like("%" + search + "%")),Article.sort.desc(),page,10)
    return render_template("admin/article/article_list.html",
                           category_id=category_id,
                           article_data=article_data,
                           article_category = article_category,
                           tag_data = tag_data,
                           )


# 修改文章
@admin.route("/article/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def article_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Article, getdata["id"])
        article_data = object_to_dict(data)
        #替换掉产品数据里面的TAGS
        tags = Crud.search_data(TagRelation,and_(TagRelation.relation_id==getdata["id"] , TagRelation.tag_type == 2),'create_time')
        if tags:
            article_data['tags'] = [v.tag_id for v in tags]
        return {"code": 1, "data": article_data}
    elif request.method == "PUT":
        data = request.form
        form = ArticleForm(data)
        if form.validate():
            #移除已保存的tag
            tags = Crud.search_data(TagRelation,and_(TagRelation.relation_id==data["id"] , TagRelation.tag_type == 2),'create_time')
            if tags:
                del_tags = Crud.clean_all(tags)
            #保存修改后的信息
            result = Crud.update(Article,data)
            # 如果有标签信息，根据产品的id和标签ID保存关联的标签数据
            if data['tags']:
                tags = data['tags'].split(',') 
                tag_data = [TagRelation(
                    tag_type = 2,
                    relation_id = data["id"],
                    tag_id =v
                ) for v in tags]
                Crud.add_all(tag_data)
            if result:
                op_log("修改文章 #%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误'} 
        return {"code": 0, "msg": form.get_errors()}



# 删除文章
@admin.route("/article/del", methods=['DELETE'])
@login_required
@auth_required
def article_del():
    deldata = request.form
    data = Article.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除文章-%s" % data.title)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败'}    