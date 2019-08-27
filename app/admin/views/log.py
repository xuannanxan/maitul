# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from .. import admin
from flask import  render_template
from flask_login import login_required
from app.models import Operationlog,Admin,Adminlog,Userlog,Crud
from app.expand.utils import Pagination

# 操作日志
@admin.route("/operation/log/<int:page>", methods=["GET"])
@admin.route("/operation/log", methods=["GET"])
@login_required
def operation_log(page=None):
    if page is None:
        page = 1
    sql = '''
        SELECT operationlog.id,operationlog.create_time,operationlog.ip,admin.username,operationlog.reason
        FROM operationlog LEFT JOIN admin ON operationlog.admin_id = admin.id
        WHERE operationlog.is_del = 0 
        ORDER BY operationlog.create_time DESC
        LIMIT %d,%d
    '''%(page*10-9,10)
    data = Crud.auto_commit(sql)
    count = Operationlog.query.filter(Operationlog.is_del == 0).count()
    page_data = Pagination(page,10,count,data.fetchall())
    return render_template("admin/log/operation_log.html", page_data=page_data)


# 管理员登录日志
@admin.route("/admin/log/<int:page>", methods=["GET"])
@admin.route("/admin/log", methods=["GET"])
@login_required
def admin_log(page=None):
    if page is None:
        page = 1
    sql = '''
        SELECT adminlog.id,adminlog.create_time,adminlog.ip,admin.username
        FROM adminlog LEFT JOIN admin ON adminlog.admin_id = admin.id
        WHERE adminlog.is_del = 0 
        ORDER BY adminlog.create_time DESC
        LIMIT %d,%d
    '''%(page*10-9,10)
    data = Crud.auto_commit(sql)
    count = Adminlog.query.filter(Adminlog.is_del == 0).count()
    page_data = Pagination(page,10,count,data.fetchall())
 
    return render_template("admin/log/admin_log.html", page_data=page_data)


# 用户登录日志
@admin.route("/user/log/<int:page>", methods=["GET"])
@admin.route("/user/log", methods=["GET"])
@login_required
def user_log(page=None):
    return render_template("admin/log/user_log.html", page_data=page_data)