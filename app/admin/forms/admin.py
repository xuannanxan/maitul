# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import  PasswordField,StringField,IntegerField
from wtforms.validators import DataRequired, Length

from app.expand.utils import error_to_string


# 修改密码表单，只用于验证
class ChangepwdForm(FlaskForm):
    old_pwd = PasswordField(
            validators=[
                DataRequired("请输入原密码！"),
                Length(4, 20, "原密码长度错误！")]
    )
    password = PasswordField(
            validators=[
                DataRequired("请输入新密码！"),
                Length(4, 20, "新密码长度错误！")]
    )
    r_pwd = PasswordField(
            validators=[
               DataRequired("请重复新密码！"),
                Length(4, 20, "重复新密码长度错误！")]
    )

    def get_errors(self):
        return error_to_string(self.errors.values())

# 管理员管理的表单，只用于验证
class AdminForm(FlaskForm):
    username = StringField(
            validators=[
                DataRequired("请输入用户名！"),
                Length(4, 20, "用户名长度错误！")]
    )
    password = PasswordField(
            validators=[
                DataRequired("密码不能为空！"),
                Length(4, 20, "密码长度错误！")]
    )
    role_id = IntegerField(
            validators=[
               DataRequired("请选择角色！")]
    )

    def get_errors(self):
        return error_to_string(self.errors.values())