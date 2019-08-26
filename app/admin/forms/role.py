# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length

from app.expand.utils import error_to_string


# 权限表单，只用于验证
class AuthForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入权限名称！"),
                Length(1, 20, "权限名称太长了！")]
    )
    menu_id = IntegerField(
            validators=[
                DataRequired("请选择所属菜单！")]
    )
    url = StringField(
            validators=[
                DataRequired("请输入需授权访问URL！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())

# 角色表单，只用于验证
class RoleForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入角色名称！"),
                Length(1, 20, "角色名称太长了！")]
    )
    auths = StringField(
            validators=[
                DataRequired("请选择权限！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())