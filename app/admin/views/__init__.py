# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from datetime import datetime
from flask_login import current_user
from flask import request
from app.expand.utils import build_tree,object_to_dict
from app.models import Crud,Menu,Conf,Admin,Role,Auth
from app.models.base import db
from .. import admin


# 上下文处理器
@admin.context_processor
def tpl_extra():
    menu_data = Crud.get_data(Menu, Menu.sort.desc())
    rule = str(request.url_rule)
    #用户权限列表
    auth_urls = []
    if  hasattr(current_user, 'id'):
        if current_user.id != 1:
            sql = '''
            SELECT url 
            FROM auth LEFT JOIN role ON FIND_IN_SET(auth.id,role.auths) LEFT JOIN admin ON admin.role_id = role.id
            WHERE admin.id = %i AND auth.is_del = 0
            '''%(current_user.id)
            data = Crud.auto_commit(sql)
            #etchall() 获取所有的数据，返回类型  RowProxy 数组
            auth_urls = [v.url for v in data.fetchall()]
    # 如果有分页，去掉分页标签
    has_pagination = rule.find("<")
    if has_pagination>0:
        rule = rule[0:has_pagination-1]
    #获取当前菜单信息，用于页面展示
    active_menu = Menu.query.filter(Menu.url == rule).first()
    #配置项
    conf_model_data = Crud.get_data(Conf, Conf.sort.desc())
    conf_data,webconfig = [],{}
    for v in conf_model_data:
        conf = object_to_dict(v)
        if conf['optional_values']:
            conf['optional_values'] = (conf['optional_values']).split(',')
        conf_data.append(conf)
        webconfig[conf['ename']] = conf['default_value']
    data = dict(
            online_time= datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            menu_tree=build_tree(menu_data, 0, 0),
            rule = rule,
            active_menu = active_menu,
            conf_data = conf_data,
            webconfig = webconfig,
            auth_urls = auth_urls
    )
    return data