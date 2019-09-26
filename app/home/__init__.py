# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#导入蓝图模块
from flask import Blueprint
home = Blueprint("home",__name__)
import app.home.views.index
import app.home.views.base