# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from .. import admin
from flask import  render_template
from flask_login import login_required
from app.models import Operationlog,Admin,Adminlog,Userlog,Crud
class page_data:
    pass

# 操作日志
@admin.route("/operation/log/<int:page>", methods=["GET"])
@admin.route("/operation/log", methods=["GET"])
@login_required
def operation_log(page=None):
    if page is None:
        page = 1
    page_data = Operationlog.query.join(
            Admin
    ).filter(
            Admin.id == Operationlog.admin_id
    ).order_by(
            Operationlog.addtime.desc()
    ).paginate(page=page, per_page=10)
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
    '''%(page*10-9,page*10)
    data = Crud.auto_commit(sql)
    page_data.items = data.fetchall()
    page_data.prev_num = page
    page_data.next_num = page+1
    page_data.iter_pages = '10'
    return render_template("admin/log/admin_log.html", page_data=page_data)


# 用户登录日志
@admin.route("/user/log/<int:page>", methods=["GET"])
@admin.route("/user/log", methods=["GET"])
@login_required
def user_log(page=None):
    return render_template("admin/log/user_log.html", page_data=page_data)