# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import ProductForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict,build_tree
from app.models import Product,Crud,Category,Tag,TagRelation,and_
from .. import admin


# 添加产品
@admin.route("/product/add", methods=['POST'])
@login_required
@auth_required
def product_add():
    data = request.form
    form = ProductForm(data)
    if form.validate():
        # 先添加产品信息  
        product_data = Crud.add(Product,data)
        if product_data:
            # 如果有标签信息，根据产品的id和标签ID保存关联的标签数据
            if data['tags']:
                tags = data['tags'].split(',') 
                tag_data = [TagRelation(
                    tag_type = 1,
                    relation_id = product_data.id,
                    tag_id =v
                ) for v in tags]
                Crud.add_all(tag_data)
            op_log("添加产品-%s" % product_data.title)
            return {"code": 1, "msg": "添加成功"}
        return {"code": 0, "msg": '添加失败，系统错误'}
    return {"code": 0, "msg": form.get_errors()}


# 产品列表
@admin.route("/product/list", methods=['GET'])
@login_required
@auth_required
def product_list():
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
    product_category = [v  for v in category_tree if v['type'] == 1 or v['type'] == 3 ]
    if category_id == None:
        product_data = Crud.search_data_paginate(Product,Product.title.like("%" + search + "%"),Product.sort.desc(),page,10)
    else:
        product_data = Crud.search_data_paginate(Product,and_(Product.category_id == category_id,Product.title.like("%" + search + "%")),Product.sort.desc(),page,10)
    return render_template("admin/product/product_list.html",
                           category_id=category_id,
                           product_data=product_data,
                           product_category = product_category,
                           tag_data = tag_data,
                           )


# 修改产品
@admin.route("/product/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def product_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Product, getdata["id"])
        product_data = object_to_dict(data)
        #替换掉产品数据里面的TAGS
        tags = Crud.search_data(TagRelation,and_(TagRelation.relation_id==getdata["id"] , TagRelation.tag_type == 1),'create_time')
        if tags:
            product_data['tags'] = [v.tag_id for v in tags]
        return {"code": 1, "data": product_data}
    elif request.method == "PUT":
        data = request.form
        form = ProductForm(data)
        if form.validate():
            #移除已保存的tag
            tags = Crud.search_data(TagRelation,and_(TagRelation.relation_id==data["id"] , TagRelation.tag_type == 1),'create_time')
            if tags:
                del_tags = Crud.clean_all(tags)
            #保存修改后的信息
            result = Crud.update(Product,data)
            # 如果有标签信息，根据产品的id和标签ID保存关联的标签数据
            if data['tags']:
                tags = data['tags'].split(',') 
                tag_data = [TagRelation(
                    tag_type = 1,
                    relation_id = data["id"],
                    tag_id =v
                ) for v in tags]
                Crud.add_all(tag_data)
            if result:
                op_log("修改产品 #%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误'} 
        return {"code": 0, "msg": form.get_errors()}


# 删除产品
@admin.route("/product/del", methods=['DELETE'])
@login_required
@auth_required
def product_del():
    deldata = request.form
    data = Product.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除产品-%s" % data.title)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败'}    