# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import AdminForm
from app.admin.views.base import op_log,auth_required
from app.models import Admin,Crud,Role
from .. import admin


# 添加管理员
@admin.route("/admin/add", methods=["POST"])
@login_required
@auth_required
def admin_add():
    data = request.form
    form = AdminForm(data)
    if form.validate():
        result = Crud.add(Admin,data,"username")
        op_log("添加管理员-%s" % data["username"])
    else:
        result = {"code": 2, "msg": form.get_errors()}
    return jsonify(result)


# 管理员列表
@admin.route("/admin/list/<int:page>", methods=['GET'])
@admin.route("/admin/list", methods=['GET'])
@login_required
@auth_required
def admin_list(page=None):
    page_data = Crud.get_data_paginate(Admin, "addtime", page, 10)
    role_data = Crud.get_data(Role,'addtime')
    return render_template("admin/admin/admin_list.html", page_data=page_data,role_data = role_data)


# 修改管理员
@admin.route("/admin/reset", methods=['GET'])
@login_required
@auth_required
def admin_reset():
        getdata = request.args
        data = Crud.get_data_by_id(Admin, getdata['id'])
        data.password = "123456"
        result = Crud.easy_update(data)
        op_log("重置密码")
        return jsonify({"code": 1, "msg": "重置密码成功！"})


# 删除管理员
@admin.route("/admin/del", methods=['DELETE'])
@login_required
@auth_required
def admin_del():
    deldata = request.form
    data = Admin.query.filter_by(id=deldata['id']).first_or_404()
    if data.is_super != 1:
        result = Crud.delete(data)
        op_log("删除管理员-%s" % data.username)
    else:
        result = {"code": 2, "msg": "不能删除超级管理员！"}
    return jsonify(result)
