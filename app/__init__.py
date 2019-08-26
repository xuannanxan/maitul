# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.

from flask import Flask,render_template
from app.extensions import config_extensions
import logging,os,time
from logging.handlers import RotatingFileHandler
from .admin import admin
from .home import home
from app.expand.utils import make_dir
DEFAULT_BLUEPRINT = (
    (admin,'/admin'),
    (home,'')

)

def app_log(app):
    log_dir_name = "logs"
    log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name
    make_dir(log_file_folder)
    log_file_str = log_file_folder + os.sep + log_file_name
    log_level = logging.INFO
    handler = logging.FileHandler(log_file_str, encoding='UTF-8')
    handler.setLevel(log_level)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

# 封装配置蓝本的函数
def config_blueprint(app):
    # 循环读取元组中的蓝本
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("common/404.html"),404

def config_errorhandler(app):
    # 如果在蓝本定制，则只针对蓝本的错误有效。
    # 可以使用app_errorhandler定制全局有效的错误显示
    # 定制全局404错误页面
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('admin/404.html',e=e)

# 将创建app的动作封装成一个函数
def create_app():
    # 创建app实例对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object( 'app.config')
    app.config.from_object( 'app.secure')
    app_log(app)
    # 加载扩展
    config_extensions(app)

    # 配置蓝本
    config_blueprint(app)


    # 配置全局错误处理
    config_errorhandler(app)

    # 返回app实例对象
    return app