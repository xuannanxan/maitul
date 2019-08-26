# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.views.base import op_log,auth_required
from app.models import Message,Crud
from .. import admin


# 留言列表
@admin.route("/message/list/<int:page>", methods=['GET'])
@admin.route("/message/list", methods=['GET'])
@login_required
@auth_required
def message(page=None):
    page_data = Crud.get_data_paginate(Message, Message.create_time.desc(), page, 10)
    return render_template("admin/message/message.html", page_data=page_data)


# 删除标签
@admin.route("/message/del", methods=['DELETE'])
@login_required
@auth_required
def message_del():
    deldata = request.form
    data = Message.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    op_log("删除留言-%s" % data.name)
    return jsonify(result)
