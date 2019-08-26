# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length

from app.expand.utils import error_to_string


class MenuForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入菜单名称！"),
                Length(1, 20, "菜单名称太长了！")]
    )
    sort = IntegerField(
            validators=[
                DataRequired("请输入排序号！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())