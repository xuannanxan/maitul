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
        '''
        temp_data{
            temp:模板设置内容
            data：{当前栏目数据
                sub_category：子栏目数据 
                sub_data：子栏目数据 
                tag:所有标签数据
            }
        }

        '''
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
                tableName = 'product'
            # 如果是文章
            if data['type'] == 2:
                tableName = 'article'
            # 如果是关联查询，就是通过   relation_id 进行搜索 
            if v.relation:
                selectColumn = 'relation_id'
            # 如果不是关联查询，就是通过   category_id 进行搜索 
            else:
                selectColumn = 'category_id'
            data['sub_data'] = selectSubData(tableName,selectColumn,cates,page,v.data_num)
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



def selectSubData(tableName,selectColumn,selectList,page,num):
    '''
    tableName:表名
    selectColumn：筛选的字段
    selectList：IN查询的数组
    page:页面
    num:页面数量
    '''
    sql='''
        SELECT SQL_CALC_FOUND_ROWS p.*,GROUP_CONCAT(t.id SEPARATOR ',') as tags
        FROM %s as p
            left join tag_relation as r on p.id = r.relation_id
            left join tag as t on t.id = r.tag_id
        WHERE p.%s in (%s)
        GROUP BY p.id
        ORDER BY p.sort DESC
        LIMIT %d,%d;
        '''%(tableName,selectColumn,(','.join([str(v) for v in  selectList])),(page-1)*num,num)
    sql_data = Crud.auto_select(sql)
    count_num = Crud.auto_select("SELECT FOUND_ROWS() as countnum")
    count = int((count_num.fetchone()).countnum)
    if sql_data:
        return Pagination(page,num,count,sql_data.fetchall())
    return {}
