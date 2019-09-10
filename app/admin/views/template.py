# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import TemplateForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict,build_tree
from app.models import Category,Crud,Template,Adspace
from .. import admin


# 添加模板
@admin.route("/template/add", methods=["POST"])
@login_required
@auth_required
def template_add():
    data = request.form
    form = TemplateForm(data)
    if form.validate():
        result = Crud.add(Template,data,"name")
        if result:
            op_log("添加模板-%s" % data["name"])
            return {"code": 1, "msg": '添加成功'}
        return {"code": 0, "msg": '添加失败，系统错误或分类已存在'}
    return {"code": 0, "msg": form.get_errors()}


# 模板列表
@admin.route("/template/list", methods=['GET'])
@admin.route("/template/list/<int:nav_id>", methods=['GET'])
@login_required
@auth_required
def template_list(nav_id=None):
    data = Crud.get_data(Category, Category.sort.desc())
    nav_tree = build_tree(data, 0, 0)
    if nav_id == None:
        template_data = Crud.get_data(Template,Template.sort.desc())
    else:
        template_data = Crud.search_data(Template,Template.nav_id == nav_id,Template.sort.desc())
    return render_template("admin/template/template_list.html",
                           nav_tree=nav_tree,
                           template_data=template_data,
                           nav_id=nav_id
                           )


# 修改模板
@admin.route("/template/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def template_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Template, getdata['id'])
        return {"code": 1, "data": object_to_dict(data)}
    elif request.method == "PUT":
        data = request.form
        form = TemplateForm(data)
        if form.validate():
            result = Crud.update(Template,data,"name")
            if result:
                op_log("修改模板#%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误或名称已存在'}
        return {"code": 0, "msg": form.get_errors()}


# 删除模板
@admin.route("/template/del", methods=['DELETE'])
@login_required
@auth_required
def template_del():
    deldata = request.form
    data = Template.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除模板-%s" % data.name)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败，请重试'}
