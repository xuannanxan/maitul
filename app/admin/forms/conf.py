# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length,InputRequired

from app.expand.utils import error_to_string


# 标签表单，只用于验证
class ConfForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入配置项名称！"),
                Length(1, 20, "配置项名称太长了！")]
    )
    ename = StringField(
            validators=[
                DataRequired("请输入配置项调用名称！"),
                Length(1, 20, "配置项调用名称太长了！")]
    )
    type = IntegerField(
            validators=[
                InputRequired("请选择配置项类型！")]
    )
    sort = IntegerField(
            validators=[
                InputRequired("请输入排序号！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())