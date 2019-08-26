# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.expand.utils import error_to_string


# 标签表单，只用于验证
class ReptileForm(FlaskForm):
    name = StringField(
            validators=[
                DataRequired("请输入爬虫任务名称！"),
                Length(1, 20, "任务名称太长了！")]
    )
    url = StringField(
            validators=[
                DataRequired("请输入要爬取的URL！"),
                Length(1, 255, "URL太长了！")]
    )
    dom = StringField(
            validators=[
                DataRequired("请输入要爬取的URL！"),
                Length(1, 255, "URL太长了！")]
    )
    content_name = StringField(
            validators=[
                DataRequired("请输入内容名称爬取规则"),
                Length(1, 255, "内容名称爬取规则太长了！")]
    )
    content_main = StringField(
            validators=[
                DataRequired("请输入主内容爬取规则"),
                Length(1, 255, "主内容爬取规则太长了！")]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())