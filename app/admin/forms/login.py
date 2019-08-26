# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-25.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length
# 登录表单
class LoginForm(FlaskForm):
    username = StringField(
            label="用户名",
            validators=[
                DataRequired("请输入用户名！"),
                Length(4, 20, "用户名长度错误！")
            ],
            description="用户名",
            render_kw={
                "class": "form-control",
                "placeholder": "请输入用户名",
                "required": "required"
            }
    )
    password = PasswordField(
            label="密码",
            validators=[
                DataRequired("请输入密码！"),
                Length(4, 20, "密码长度错误！")
            ],
            description="密码",
            render_kw={
                "class": "form-control",
                "placeholder": "请输入密码",
                "required": "required"
            }
    )
    submit = SubmitField(
            "登录",
            render_kw={
                "class": "btn btn-info btn-block",
            }
    )


# 移动端登录表单
class MobileLoginForm(FlaskForm):
    username = StringField(
            label="用户名",
            validators=[
                DataRequired("请输入用户名！"),
                Length(4, 20, "用户名长度错误！")
            ],
            description="用户名",
            render_kw={
                "class": "weui-input",
                "placeholder": "请输入用户名",
                "required": "required"
            }
    )
    password = PasswordField(
            label="密码",
            validators=[
                DataRequired("请输入密码！"),
                Length(4, 20, "密码长度错误！")
            ],
            description="密码",
            render_kw={
                "class": "weui-input",
                "placeholder": "请输入密码",
                "required": "required"
            }
    )
    submit = SubmitField(
            "登录",
            render_kw={
                "class": "weui-btn weui-btn_primary",
            }
    )
