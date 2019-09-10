# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from flask import render_template,g,request
from app.expand.utils import object_to_dict
from app.models import Crud,Product,Category,Template,Ad,Article
from . import home,seo_data,cache,getTemplate,getCategory,getTemplates,getTag


@home.route("/", methods=['GET'])
@home.route("/<int:nav_id>", methods=['GET'])
@home.route("/<int:nav_id>/<int:cate_id>", methods=['GET'])
@home.route("/<int:nav_id>/<int:cate_id>/<int:content_id>", methods=['GET'])
#@cache.cached(key_prefix='index')#设置一个key_prefix来作为标记,调用cache.delete('index')来删除缓存来保证用户访问到的内容是最新的
def index(nav_id=None,cate_id=None,content_id=None):
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
        # 页码
    page,artpage = 1,1
    if request.args.get('page'):
        page = int(request.args.get('page'))   
    if request.args.get('artpage'):
        page = int(request.args.get('artpage'))     
    param = {
        'nav_id':nav_id,
        'cate_id':cate_id,
        'content_id':content_id
    }
    all_templates = getTemplates()
    if nav_id:
        templates_data = [v for v in all_templates if v.nav_id==nav_id]
    else:
        templates_data = [v for v in all_templates if v.nav_id==0]
    templates = []
    category_data = getCategory()
    for v in templates_data:
        temp_data,data = {},{}
        temp_data['temp'] = object_to_dict(v)
        sub_category,cates = [],[]
        for val in category_data:   
            if v.data_id:
                # 如果分配了数据当前栏目的数据就是分配的栏目
                if val.id == v.data_id:
                    data = object_to_dict(val)
                # 当前栏目的子栏目
                if val.pid == v.data_id:
                    sub_category.append(val)
                data['sub_category'] = sub_category
            # 如果没有数据，赋值菜单数据
            else:
                if val.id == v.nav_id:
                    data = object_to_dict(val)
        #如果是栏目数据
        if v.data_type == 1: 
            if cate_id:
                # url传了分类id
                cates.append(cate_id)
                cates = cates+[cate.id for cate in category_data if cate.pid == cate_id]
            else:
                # URL没有传分类id，读取设置的数据
                cates.append(v.data_id)
                cates = cates+[cate.id for cate in sub_category]        
            # 如果是产品
            if data['type'] == 1:
                sub_data = Crud.search_data_paginate(Product,Product.category_id.in_(cates),Product.sort.desc(),page,v.data_num)
            # 如果是文章
            if data['type'] == 2:
                sub_data = Crud.search_data_paginate(Article,Article.category_id.in_(cates),Article.sort.desc(),artpage,v.data_num)
            data['sub_data'] = sub_data
        elif v.data_type == 2:
            data = Crud.search_data(Ad,Ad.space_id == v.data_id,Ad.sort.desc(),v.data_num)
        elif v.data_type == 3:
            data = getTag()
        temp_data['data'] = data
        # 全部页面数据压入数组
        templates.append(temp_data)
    return render_template("home/%s/home.html"%getTemplate(),
        seo_data = seo_data,
        templates = templates,
        param = param
    )

