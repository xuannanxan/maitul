# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import CategoryForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict,build_tree
from app.models import Category,Crud
from .. import admin


# 添加分类
@admin.route("/category/add", methods=["POST"])
@login_required
@auth_required
def category_add():
    data = request.form
    form = CategoryForm(data)
    if form.validate():
        result = Crud.add(Category,data,"name")
        if result:
            op_log("添加分类-%s" % data["name"])
            return {"code": 1, "msg": '添加成功'}
        return {"code": 0, "msg": '添加失败，系统错误或分类已存在'}
    return {"code": 0, "msg": form.get_errors()}


# 分类列表
@admin.route("/category/list", methods=['GET'])
@admin.route("/category/list/<int:pid>", methods=['GET'])
@login_required
@auth_required
def category_list(pid=None):
    data = Crud.get_data(Category, Category.sort.desc())
    category_tree = build_tree(data, 0, 0)
    if pid == None:
        category_data = category_tree
    else:
        category_data = [v for v in data if v.pid==pid]
    return render_template("admin/category/category_list.html",
                           category_tree=category_tree,
                           category_data=category_data,
                           pid=pid
                           )


# 修改分类
@admin.route("/category/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def category_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Category, getdata['id'])
        return {"code": 1, "data": object_to_dict(data)}
    elif request.method == "PUT":
        data = request.form
        form = CategoryForm(data)
        if form.validate():
            result = Crud.update(Category,data,"name")
            if result:
                op_log("修改分类#%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误或名称已存在'}
        return {"code": 0, "msg": form.get_errors()}


# 删除分类
@admin.route("/category/del", methods=['DELETE'])
@login_required
@auth_required
def category_del():
    deldata = request.form
    
    child_category_count = Category.query.filter(Category.pid==deldata['id'], Category.is_del == 0).count()
    
    if child_category_count>0:
        return {"code": 2, "msg": '当前分类包含子分类，删除失败！'}
    else:
        data = Category.query.filter_by(id=deldata['id']).first_or_404()
        result = Crud.delete(data)
        if result:
            op_log("删除分类-%s" % data.name)
            return {"code": 1, "msg": '删除成功'}
        return {"code": 0, "msg": '删除失败，请重试'}
