# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__ador__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import AdspaceForm,AdForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict
from app.models import Adspace,Crud,Ad
from .. import admin


# 添加广告位
@admin.route("/adspace/add", methods=["POST"])
@login_required
@auth_required
def adspace_add():
    data = request.form
    form = AdspaceForm(data)
    if form.validate():
        result = Crud.add(Adspace,data,"name")
        if result:
            op_log("添加广告位-%s" % data["name"])
            return {"code": 1, "msg": '添加成功'}
        return {"code": 0, "msg": '添加失败，系统错误或名称已存在'}    
    return {"code": 0, "msg": form.get_errors()}
    

# 广告位列表
@admin.route("/adspace/list", methods=['GET'])
@login_required
@auth_required
def adspace_list():
    list_data = Crud.get_data(Adspace, 'create_time')
    return render_template("admin/adspace/adspace_list.html", list_data=list_data)


# 修改广告位
@admin.route("/adspace/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def adspace_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Adspace, getdata['id'])
        return  {"code": 1, "data": object_to_dict(data)}
    elif request.method == "PUT":
        data = request.form
        form = AdspaceForm(data)
        if form.validate():
            result = Crud.update(Adspace,data,"name")
            if result:
                op_log("修改广告位#%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误或名称已存在'}    
        return {"code": 0, "msg": form.get_errors()}


# 删除广告位
@admin.route("/adspace/del", methods=['DELETE'])
@login_required
@auth_required
def adspace_del():
    deldata = request.form
    data = Adspace.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除广告位-%s" % data.name)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败，系统错误'} 

# 添加广告
@admin.route("/ad/add", methods=['POST'])
@login_required
@auth_required
def ad_add():
    data = request.form
    form = AdForm(data)
    if form.validate():
        result = Crud.add(Ad,data,'title')
        if result:
            op_log("添加广告-%s" % data["title"])
            return {"code": 1, "msg": '添加成功'}
        return {"code": 0, "msg": '添加失败，系统错误或名称已存在'}    
    return {"code": 0, "msg": form.get_errors()}

# 广告列表
@admin.route("/ad/list", methods=['GET'])
@admin.route("/ad/list/<int:space_id>", methods=['GET'])
@login_required
@auth_required
def ad_list(space_id=None):
    sapce_data= Crud.get_data(Adspace)
    if space_id == None:
        ad_data = Crud.get_data(Ad,Ad.sort.desc())
    else:
        ad_data = Crud.search_data(Ad,Ad.space_id == space_id,Ad.sort.desc())
    return render_template("admin/ad/ad_list.html", space_id=space_id,ad_data=ad_data,sapce_data=sapce_data)
# 修改广告
@admin.route("/ad/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def ad_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Ad, getdata["id"])
        return {"code": 1, "data": object_to_dict(data)}
    elif request.method == "PUT":
        data = request.form
        form = AdForm(data)
        if form.validate():
            result = Crud.update(Ad,data,'title')
            if result:
                op_log("修改广告 #%s" %  data["id"])
                return {"code": 1, "msg": '修改成功'}
            return {"code": 0, "msg": '修改失败，系统错误或名称已存在'}    
        return {"code": 0, "msg": form.get_errors()}

        
# 删除广告
@admin.route("/ad/del", methods=['DELETE'])
@login_required
@auth_required
def ad_del():
    deldata = request.form
    data = Ad.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除广告-%s" % data.title)
        return {"code": 1, "msg": '删除成功'}
    return {"code": 0, "msg": '删除失败，系统错误'}    