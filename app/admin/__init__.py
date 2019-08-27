# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#导入蓝图模块
from flask import Blueprint
admin = Blueprint("admin",__name__)
import app.admin.views.base
import app.admin.views.tag
import app.admin.views.log
import app.admin.views.menu
import app.admin.views.role
import app.admin.views.auth
import app.admin.views.admin
import app.admin.views.category
import app.admin.views.article
import app.admin.views.product
import app.admin.views.ad
import app.admin.views.conf
import app.admin.views.reptile
import app.admin.views.message


