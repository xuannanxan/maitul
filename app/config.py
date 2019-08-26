# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-02.
import os,time

# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
WATER_MARK = os.path.join(BASE_DIR, 'static/admin/img/watermark.png')
FILE_EXTENSIONS = set(['txt', 'pdf','rar', 'zip','doc', 'docx','xls', 'xlsx', 'ppt', 'pptx','db','png', 'jpg', 'jpeg', 'gif'])
IMAGE_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
    # 数据库公用配置
    # 无警告
SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 自动提交
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 发邮件 配置
MAIL_USE_SSL = True
MAIL_SUPPRESS_SEND = False
MAIL_PORT = 465
MAIL_USE_TLS = False
#设置simple缓存类型
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300
    #文件上传的位置
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
