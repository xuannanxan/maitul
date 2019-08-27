# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import MenuForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict
from app.models import Menu,Crud
from .. import admin


# 添加菜单
@admin.route("/menu/add", methods=["POST"])
@login_required
@auth_required
def menu_add():
    data = request.form
    form = MenuForm(data)
    if form.validate():
        result = Crud.add(Menu,data,'name')
        if result:
            op_log("添加菜单-%s" % data["name"])
            return {"code": 1, "msg": "添加成功！"}
        return {"code": 0, "msg": "添加失败，系统错误或菜单已存在"}
    return {"code": 0, "msg": form.get_errors()}



# 菜单列表
@admin.route("/menu/list", methods=['GET'])
@login_required
@auth_required
def menu_list():
    return render_template("admin/menu/menu_list.html")


# 修改菜单
@admin.route("/menu/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def menu_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Menu, getdata['id'])
        return jsonify({"code": 1, "data": object_to_dict(data)})
    elif request.method == "PUT":
        data = request.form
        form = MenuForm(data)
        if form.validate():
            result = Crud.update(Menu,data,'name')
            if result:
                op_log("修改菜单#%s" %  data["id"])
                return {"code": 1, "msg": "修改成功！"}
            return {"code": 0, "msg": "修改失败，系统错误或菜单已存在"}
        return {"code": 0, "msg": form.get_errors()}


# 删除菜单
@admin.route("/menu/del", methods=['DELETE'])
@login_required
@auth_required
def menu_del():
    deldata = request.form
    child_category_count = Menu.query.filter_by(pid=deldata['id']).count()
    if child_category_count>0:
        result = {"code": 2, "msg": '当前菜单包含子菜单，删除失败！'}
    else:
        data = Menu.query.filter_by(id=deldata['id']).first_or_404()
        result = Crud.delete(data)
        if result:
            op_log("删除菜单-%s" % data.name)
            return {"code": 1, "msg": "删除成功！"}
        return {"code": 0, "msg": "删除失败，系统错误"}