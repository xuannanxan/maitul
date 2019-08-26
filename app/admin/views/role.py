# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import AuthForm,RoleForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict
from app.models import Auth,Menu,Role,Crud
from .. import admin


# 角色列表
@admin.route("/role/list",methods = ['GET'])
@admin.route("/role/list/<int:page>",methods = ['GET'])
@login_required
@auth_required
def role_list(page=None):
    menu_auths = Menu.query.join(
        Auth
    ).filter(
        Menu.id == Auth.menu_id
    ).order_by(
        Menu.sort.desc()
    ).all()
    for v in menu_auths:
        auths = v.auths # 读取auths才能获取到数据
    page_data = Crud.get_data_paginate(Role, Role.addtime.desc(), page, 10)
    return render_template("admin/role/role_list.html",page_data = page_data,menu_auths = menu_auths)


# 添加角色
@admin.route("/role/add",methods = ['POST'])
@login_required
@auth_required
def role_add():
    data = request.form
    form = RoleForm(data)
    if form.validate():
        result = Crud.add(Role,data,'name')
        op_log("添加角色-%s" % data["name"])
    else:
        result = {"code": 2, "msg": form.get_errors()}
    return jsonify(result)
# 修改角色
@admin.route("/role/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def role_edit():
    if request.method == 'GET':
        getdata = request.args
        if int(getdata["id"]) == 1:
            return jsonify({"code": 2, "msg": "超级管理员不能修改！"})
        data = Crud.get_data_by_id(Role, getdata["id"])
        # auth_list = list(map(lambda v:int(v),(data.auths).split(",")))
        auth_list = (data.auths).split(",")
        role_data = {"name": data.name,"id":data.id, "auths": auth_list}
        return jsonify({"code": 1, "data": role_data})
    elif request.method == "PUT":
        data = request.form
        form = RoleForm(data)
        if form.validate():
                result = Crud.update(Role,data,'name')
                op_log("修改角色 #%s" %  data["id"])
        else:
            result = {"code": 2, "msg": form.get_errors()}
        return jsonify(result)
# 删除角色
@admin.route("/role/del", methods=['DELETE'])
@login_required
@auth_required
def role_del():
    delData = request.form
    if int(delData['id']) == 1:
            return jsonify({"code": 2, "msg": "超级管理员不能删除！"})
    data = Role.query.filter_by(id=delData['id']).first_or_404()
    result = Crud.delete(data)
    op_log("删除角色-%s" % data.name)
    return jsonify(result)
