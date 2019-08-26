# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField,FloatField
from wtforms.validators import DataRequired, Length,InputRequired

from app.expand.utils import error_to_string


# 标签表单，只用于验证
class ProductForm(FlaskForm):
    title = StringField(
            validators=[
                DataRequired("请输入产品名称！"),
                Length(1, 50, "名称不能超过50个字！")]
    )
    sort = IntegerField(
            validators=[
                InputRequired("请输入排序号！")]
    )
    description = StringField(
            validators=[
                Length(0, 255, "描述不能超过255个字！")]
    )
    price = FloatField(
            validators=[
                InputRequired("请输入价格！")]
    )
    category_id = IntegerField(
            validators=[
                DataRequired("请选择分类！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())