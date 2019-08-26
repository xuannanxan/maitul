# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.

from flask_wtf import FlaskForm
from wtforms import  StringField
from wtforms.validators import DataRequired,Email

from app.expand.utils import error_to_string


# 邮箱表单，只用于验证
class MessageForm(FlaskForm):
    email = StringField(
            validators=[
                DataRequired("Please input your Email."),
                Email("Please input the correct Email.")
            ]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())