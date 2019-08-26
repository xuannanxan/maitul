# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import AuthForm,RoleForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict
from app.models import Auth,Crud
from .. import admin


# 添加权限
@admin.route("/auth/add", methods=['POST'])
@login_required
@auth_required
def auth_add():
    data = request.form
    form = AuthForm(data)
    if form.validate():
        result = Crud.add(Auth,data,'name')
        if result:
            op_log("添加权限-%s" % data["name"])
            return {"code": 1, "msg": '添加成功'}
        return {"code": 0, "msg": '添加失败，系统错误或名称重复'}
    return {"code": 0, "msg": form.get_errors()}



# 权限列表
@admin.route("/auth/list", methods=['GET'])
@admin.route("/auth/list/<int:menuid>", methods=['GET'])
@login_required
@auth_required
def auth_list(menuid=None):
    if menuid == None:
        auth_data = Crud.get_data(Auth)
    else:
        auth_data = Crud.search_data(Auth,Auth.menu_id == menuid)
    return render_template("admin/auth/auth_list.html", menuid=menuid,auth_data=auth_data)


# 修改权限
@admin.route("/auth/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def auth_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Auth, getdata["id"])
        return {"code": 1, "data": object_to_dict(data)}
    elif request.method == "PUT":
        data = request.form
        form = AuthForm(data)
        if form.validate():
            result = Crud.update(Auth,data,'name')
            if result:
                op_log("修改权限 #%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误或名称重复'}
        return {"code": 0, "msg": form.get_errors()}


# 删除权限
@admin.route("/auth/del", methods=['DELETE'])
@login_required
@auth_required
def auth_del():
    deldata = request.form
    data = Auth.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除权限-%s" % data.name)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败，系统错误'}