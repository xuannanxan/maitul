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
        if result['code'] == 1:
            op_log("添加广告位-%s" % data["name"])
    else:
        result = {"code": 2, "msg": form.get_errors()}
    return jsonify(result)


# 广告位列表
@admin.route("/adspace/list", methods=['GET'])
@login_required
@auth_required
def adspace_list():
    list_data = Crud.get_data(Adspace, None)
    return render_template("admin/adspace/adspace_list.html", list_data=list_data)


# 修改广告位
@admin.route("/adspace/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def adspace_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Adspace, getdata['id'])
        return jsonify({"code": 1, "data": object_to_dict(data)})
    elif request.method == "PUT":
        data = request.form
        form = AdspaceForm(data)
        if form.validate():
            result = Crud.update(Adspace,data,"name")
            op_log("修改广告位#%s" %  data["id"])
        else:
            result = {"code": 2, "msg": form.get_errors()}
        return jsonify(result)


# 删除广告位
@admin.route("/adspace/del", methods=['DELETE'])
@login_required
@auth_required
def adspace_del():
    deldata = request.form
    data = Adspace.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    op_log("删除广告位-%s" % data.name)
    return jsonify(result)


# 添加广告
@admin.route("/ad/add", methods=['POST'])
@login_required
@auth_required
def ad_add():
    data = request.form
    form = AdForm(data)
    if form.validate():
            result = Crud.add(Ad,data,'title')
            op_log("添加广告-%s" % data["title"])
    else:
        result = {"code": 2, "msg": form.get_errors()}
    return jsonify(result)


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
        return jsonify({"code": 1, "data": object_to_dict(data)})
    elif request.method == "PUT":
        data = request.form
        form = AdForm(data)
        if form.validate():
            result = Crud.update(Ad,data,'title')
            op_log("修改广告 #%s" %  data["id"])
        else:
            result = {"code": 2, "msg": form.get_errors()}
        return jsonify(result)
# 删除广告
@admin.route("/ad/del", methods=['DELETE'])
@login_required
@auth_required
def ad_del():
    deldata = request.form
    data = Ad.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    op_log("删除广告-%s" % data.title)
    return jsonify(result)