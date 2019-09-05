# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from flask import render_template,g,request
from app.expand.utils import object_to_dict
from app.models import Crud,Product,Category,Template,Ad,Article
from . import home,seo_data,cache,getTemplate,getCategory


@home.route("/")
@home.route("/<string:nav>")
#@cache.cached(key_prefix='index')#设置一个key_prefix来作为标记,调用cache.delete('index')来删除缓存来保证用户访问到的内容是最新的
def index(nav=None):
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
        # 页码
        page = 1
        if request.args.get('page'):
            page = int(request.args.get('page'))   
        #如果是栏目数据
        if v.data_type == 1:
            category_data = getCategory()
            data = [object_to_dict(val) for val in category_data if val.id == v.data_id][0]
            # 如果是产品
            if data['type'] == 1:
                product_data = Crud.get_data_paginate(Product,Product.sort.desc(),page,v.data_num)
                data['sub_data'] = product_data
            if data['type'] == 2:
                article_data = Crud.get_data_paginate(Article,Article.sort.desc(),page,v.data_num)
                data['sub_data'] = article_data
        elif v.data_type == 2:
            data = Crud.search_data(Ad,Ad.space_id == v.data_id,Ad.sort.desc(),v.data_num)
        temp_data['data'] = data
        templates.append(temp_data)
    print(templates)
    return render_template("home/%s/home.html"%getTemplate(),
        seo_data = seo_data,
        templates = templates
    )

