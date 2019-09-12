# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from flask import render_template,g,request
from app.expand.utils import object_to_dict,Pagination
from app.models import Crud,Product,Category,Template,Ad,Article
from . import home,seo_data,cache,getWebTemplate,getCategory,getTemplates,getTag


@home.route("/", methods=['GET'])
@home.route("/<int:nav_id>", methods=['GET'])
@home.route("/<int:nav_id>/<int:cate_id>", methods=['GET'])
@home.route("/<int:nav_id>/<int:cate_id>/<int:content_id>", methods=['GET'])
#@cache.cached(key_prefix='index')#设置一个key_prefix来作为标记,调用cache.delete('index')来删除缓存来保证用户访问到的内容是最新的
def index(nav_id=None,cate_id=None,content_id=None):
    # 页码
    page,artpage = 1,1
    nav_data,cate_data,content_data = {'id':nav_id},{'id':cate_id},{'id':content_id}
    category_data = getCategory()
    all_templates = getTemplates()
    if request.args.get('page'):
        page = int(request.args.get('page'))   
    if request.args.get('artpage'):
        artpage = int(request.args.get('artpage'))   
    if nav_id:
        nav_data = [v for v in category_data if v.id == nav_id][0]
        seo_data.description = nav_data.info
        seo_data.keywords = nav_data.keywords
        seo_data.title = nav_data.name
    if cate_id:
        cate_data = [v for v in category_data if v.id == cate_id][0]
        seo_data.description = cate_data.info
        seo_data.keywords = cate_data.keywords
        seo_data.title = cate_data.name
    param = {
        'nav_data':nav_data,
        'cate_data':cate_data,
        'content_data':content_data
    }
    if nav_id:
        templates_data = [v for v in all_templates if v.nav_id==nav_id]
    else:
        templates_data = [v for v in all_templates if v.nav_id==0]
    templates = []
    for v in templates_data:
        temp_data,data = {},{}
        temp_data['temp'] = object_to_dict(v)
        sub_category,cates = [],[]
        for val in category_data:   
            if v.data_id :
                if val.id == v.data_id:
                    # 如果分配了数据当前栏目的数据就是分配的栏目
                    data = object_to_dict(val)
                if v.relation:
                    # 如果是关联数据，直接取当前栏目的子栏目
                    if val.pid == nav_id:
                        sub_category.append(val)
                else:
                    # 当前栏目的子栏目
                    if val.pid == v.data_id:
                        sub_category.append(val)
        data['sub_category'] = sub_category
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
                if v.relation:
                    sub_data = Crud.search_data_paginate(Product,Product.relation_id.in_(cates),Product.sort.desc(),page,v.data_num)
                else:
                    sql='''
                    SELECT p.create_time,p.id,p.cover,p.price, p.click,p.category_id,GROUP_CONCAT(t.id,':',t.name SEPARATOR ',') as tags
                    FROM product as p
                        left join tag_relation as r on p.id = r.relation_id
                        left join tag as t on t.id = r.tag_id
                    WHERE p.category_id in (%s)
                    GROUP BY p.id
                    ORDER BY p.sort DESC
                    LIMIT %d,%d;
                    '''%((','.join([str(v) for v in  cates])),(page-1)*v.data_num+1,v.data_num)
                    sql_data = Crud.auto_commit(sql)
                    if sql_data:
                        count = (Crud.auto_commit("SELECT FOUND_ROWS() as count;")).fetchall()[0].count
                        sub_data = Pagination(page,v.data_num,count,sql_data.fetchall())
                   
                    #sub_data = Crud.search_data_paginate(Product,Product.category_id.in_(cates),Product.sort.desc(),page,v.data_num)
            # 如果是文章
            if data['type'] == 2:
                if v.relation:
                    sub_data = Crud.search_data_paginate(Article,Article.relation_id.in_(cates),Article.sort.desc(),artpage,v.data_num)
                else:
                    
                    sub_data = Crud.search_data_paginate(Article,Article.category_id.in_(cates),Article.sort.desc(),artpage,v.data_num)
            data['sub_data'] = sub_data
        elif v.data_type == 2:
            data['sub_data'] = Crud.search_data(Ad,Ad.space_id == v.data_id,Ad.sort.desc(),v.data_num)
        data['tags'] = getTag()
        temp_data['data'] = data
        # 全部页面数据压入数组
        templates.append(temp_data)
    return render_template("home/%s/home.html"%getWebTemplate(),
        seo_data = seo_data,
        templates = templates,
        param = param
    )

