# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-02-06.
__author__ = 'Allen xu'
from .. import admin
from flask import url_for,request,redirect,flash,abort,render_template,jsonify
from flask_login import login_user,login_required,logout_user,current_user
from app.models import Admin,Adminlog,Operationlog,Crud,Role,Auth
from app.admin.forms import MobileLoginForm,ChangepwdForm
from functools import wraps

# 登录
@admin.route("/m/login", methods=["GET", "POST"])
def m_login():
    form = MobileLoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(username=data["username"]).first()
        if admin and admin.check_pwd(data["password"]):
            login_user(admin)
            adminlog = Adminlog(
                    admin_id=admin.id,
                    ip=request.remote_addr
            )
            Crud.easy_add(adminlog)
            return redirect(request.args.get("next") or url_for("admin.m_index"))
        else:
            flash("用户名或密码错误！")
            return redirect(url_for("admin.m_login"))
    return render_template("admin/mobile/login.html", form=form)

@admin.route("/m")
@login_required
def m_index():
    return render_template("admin/mobile/index.html")