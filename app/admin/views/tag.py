# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import TagForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict
from app.models import Tag,Crud
from .. import admin


# 添加标签
@admin.route("/tag/add", methods=["POST"])
@login_required
@auth_required
def tag_add():
    data = request.form
    form = TagForm(data)
    if form.validate():
        add_data = Crud.add(Tag,data,"name")
        if add_data:
            op_log("添加标签-%s" % add_data.name)
            return {"code": 1, "msg": '添加成功'}
        return {"code": 0, "msg": '添加失败，系统错误或标签已存在'}
    return {"code": 0, "msg": form.get_errors()}


# 标签列表
@admin.route("/tag/list/<int:page>", methods=['GET'])
@admin.route("/tag/list", methods=['GET'])
@login_required
@auth_required
def tag_list(page=None):
    page_data = Crud.get_data_paginate(Tag, Tag.sort.desc(), page, 10)
    return render_template("admin/tag/tag_list.html", page_data=page_data)


# 修改标签
@admin.route("/tag/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def tag_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Tag, getdata['id'])
        return {"code": 1, "data": object_to_dict(data)}
    elif request.method == "PUT":
        data = request.form
        form = TagForm(data)
        if form.validate():
            result = Crud.update(Tag,data,"name")
            if result:
                op_log("修改标签#%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误或标签已存在'}    
        return {"code": 0, "msg": form.get_errors()}


# 删除标签
@admin.route("/tag/del", methods=['DELETE'])
@login_required
@auth_required
def tag_del():
    deldata = request.form
    data = Tag.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除标签-%s" % data.name)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败，请重试'}
