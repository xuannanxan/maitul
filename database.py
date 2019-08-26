# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-31.
__author__ = 'Allen xu'
import os
from werkzeug.security import check_password_hash
#主文件中导入app初始化manage
from app import create_app
# 生成app
app = create_app()

from app.extensions import db
from app.models import *
def init_data():
    password = input("即将重置数据，请输入操作密码：")
    if check_password_hash('pbkdf2:sha256:150000$WxouU1qd$82060dd41e04168e5650f9f2b75360142e98a8e65e14c24a053fd56e8b09f502',password):
        check = input("确认重置吗？重置后将失去所有历史数据，1为确认，其他为取消：")
        if check == '1':
            db.drop_all(app = app)
            db.create_all(app = app)
            print("重置成功")
        else:
            print("已取消操作")
            return
    else:
        print("密码错误，已取消操作")
        return

if __name__ == '__main__':
    init_data()