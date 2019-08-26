# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-16.

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache



# 创建对象
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()
#缓存
cache = Cache(with_jinja2_ext=False)



# 初始化
def config_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = '请先登录！！！'
    cache.init_app(app)
    #db.create_all(app = app)
    csrf.init_app(app)
    mail.init_app(app)

