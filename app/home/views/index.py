# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from flask import render_template,g
from app.expand.utils import object_to_dict
from app.models import Crud,Product,Category,Template,Ad
from . import home,seo_data,cache,getTemplate


@home.route("/")
#@cache.cached(key_prefix='index')#设置一个key_prefix来作为标记,调用cache.delete('index')来删除缓存来保证用户访问到的内容是最新的
def index():
    #  #广告
    # ad_sql = '''
    #     SELECT ad.title,ad.info,ad.img,ad.url,adspace.name,adspace.ename
    #     FROM ad LEFT JOIN adspace on ad.space_id = adspace.id
    #     WHERE ad.is_del = 0
    #     ORDER BY ad.sort DESC
    # '''
    # ads = Crud.auto_commit(ad_sql)
    # ad_data = {}
    # for v in ads.fetchall():
    #     if v.ename in ad_data:
    #         ad_data[v.ename] = ad_data[v.ename]+[v]
    #     else:
    #         ad_data[v.ename] = [v]
    templates_data = Crud.get_data(Template,Template.sort.desc())
    templates = []
    for v in templates_data:
        temp_data = object_to_dict(v)
        if v.data_type == 2:
            data = Crud.search_data(Ad,Ad.space_id == v.data_id,Ad.sort.desc(),v.data_num)
        temp_data['data'] = data
        temp_data['template_name'] = (v.template).split('.')[0]
        templates.append(temp_data)
    return render_template("home/%s/home.html"%getTemplate(),
        seo_data = seo_data,
        templates = templates
    )

