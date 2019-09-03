# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length,InputRequired

from app.expand.utils import error_to_string


# 标签表单，只用于验证
class TemplateForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入模板名称！"),
                Length(1, 50, "模板名称不能超过50个字！")]
    )
    template = StringField(
            validators=[
                DataRequired("请输入模板页面！"),
                Length(1, 100, "模板页面的名称过长")]
    )
    data_type = StringField(
            validators=[
                DataRequired("请选择数据类型！")]
    )
    sort = IntegerField(
            validators=[
                InputRequired("请输入排序号！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())