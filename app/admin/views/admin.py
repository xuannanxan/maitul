# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required
from app.expand.utils import object_to_dict
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
        if result:
            op_log("添加管理员-%s" % data["username"])
            return {"code": 1, "msg": '添加成功'}    
        return {"code": 0, "msg": '添加失败，系统错误或管理员已存在'}    
    return {"code": 0, "msg": form.get_errors()}


# 管理员列表
@admin.route("/admin/list/<int:page>", methods=['GET'])
@admin.route("/admin/list", methods=['GET'])
@login_required
@auth_required
def admin_list(page=None):
    sql = '''
    SELECT admin.id,admin.create_time,admin.username,admin.is_super,role.name as role_name,
    CASE admin.is_super 
        WHEN 1 THEN
        '超级管理员'
        ELSE
            '普通管理员'
    END as admin_type
    FROM admin LEFT JOIN role on admin.role_id = role.id
    WHERE admin.is_del = 0
    ORDER BY admin.create_time ASC
    '''
    data = Crud.auto_select(sql)
    role_data = Crud.get_data(Role,'create_time')
    return render_template("admin/admin/admin_list.html", admin_data=data.fetchall(),role_data = role_data)


# 重置管理员密码
@admin.route("/admin/reset", methods=['GET'])
@login_required
@auth_required
def admin_reset():
        getdata = request.args
        data = Crud.get_data_by_id(Admin, getdata['id'])
        data.password = "123456"
        result = Crud.easy_update(data)
        if result:
            op_log("重置密码")
            return {"code": 1, "msg": "重置密码成功！"}
        return {"code": 0, "msg": '重置失败，系统错误'}    


# 修改管理员
@admin.route("/admin/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def admin_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Admin, getdata['id'])
        return {"code": 1,"id": data.id, "role_id": data.role_id,"username": data.username}
    elif request.method == "PUT":
        data = request.form
        result = Crud.update(Admin,data)
        if result:
            op_log("修改管理员角色#%s" %  data["id"])
            return {"code": 1, "msg": '修改成功'}
        return {"code": 0, "msg": '修改失败，系统错误或管理员已存在'}    


# 删除管理员
@admin.route("/admin/del", methods=['DELETE'])
@login_required
@auth_required
def admin_del():
    deldata = request.form
    data = Admin.query.filter_by(id=deldata['id']).first_or_404()
    if data.is_super != 1:
        result = Crud.delete(data)
        if result:
            op_log("删除管理员-%s" % data.username)
            return {"code": 1, "msg": "删除成功！"}
        return {"code": 0, "msg": "删除失败，系统错误！"}
    return {"code": 0, "msg": "不能删除超级管理员！"}
