# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length,InputRequired

from app.expand.utils import error_to_string


# 标签表单，只用于验证
class CategoryForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入分类名称！"),
                Length(1, 50, "分类名称不能超过50个字！")]
    )
    ename = StringField(
            validators=[
                DataRequired("请输入调用名称！"),
                Length(1, 50, "调用名称不能超过50个字！")]
    )
    info = StringField(
            validators=[
                Length(0, 500, "描述不能超过500个字！")]
    )
    sort = IntegerField(
            validators=[
                InputRequired("请输入排序号！")]
    )
    type = IntegerField(
            validators=[
                DataRequired("请选择类型！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())