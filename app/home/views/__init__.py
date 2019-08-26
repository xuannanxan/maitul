# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.

from flask import request,current_app
from app.expand.utils import build_tree,object_to_dict,set_qrcode
from app.models import Crud,Category,Conf,Ad,Product,Tag
from .. import home
from app.extensions import cache

# cache的运行数量，通过request来进行不同cache的计数
CLICKS_COUNT = {}

class seo_data():
    keywords = ''
    description = ''
    title = ''

#获取当前栏目的最上级栏目
def getTopColumn(data,id):
    for v in data:
        if v.id == int(id):
            if int(v.pid) == 0:
                return v
            else:
                return getTopColumn(data,v.pid)

def make_cache_key(*args, **kwargs):
    """Cache的动态参数."""

    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')



# 上下文处理器
@home.context_processor
def tpl_extra():
    url =request.url
    ip=request.remote_addr
    current_app.logger.info("【%s】-%s"%(ip,url))
    webconfig,columns,tags = {},{},{'product':[],'article':[]}
    #配置项
    conf_model_data = Crud.get_data(Conf,Conf.sort.desc())
    for v in conf_model_data:
        conf = object_to_dict(v)
        if conf['values']:
            conf['values'] = (conf['values']).split(',')
        webconfig[conf['ename']] = conf['value']
    #栏目
    colums_data = Crud.get_data(Category, Category.sort.desc())
    colums_tree = build_tree(colums_data, 0, 0)
    for v in colums_tree:
        columns[v['ename']] = v
    #最近项目
    # latest_projects_column_ids = [columns['latest_project']['id']]
    # latest_projects = Crud.search_data(Product,Product.column_id.in_(latest_projects_column_ids),Product.sort.desc())
    #当前页面的nav_id
    path =request.path
    arr = path.split('/')
    nav_id = arr[2] if len(arr)>2 else ''
    #当前页面的栏目信息和当前栏目的顶级栏目
    top_nav = active_nav = ''
    if nav_id:
        top_nav = getTopColumn(colums_data,nav_id)
        active_nav = [v for v in colums_data if v.id == int(nav_id)][0]
    #广告
    ads = Crud.get_data(Ad,Ad.sort.desc())
    ad_data = {}
    for v in ads:
        if v.adspace.ename in ad_data:
            ad_data[v.adspace.ename] = ad_data[v.adspace.ename]+[v]
        else:
            ad_data[v.adspace.ename] = [v]
    #标签
    tag_data = Crud.get_data(Tag,Tag.sort.desc())
    for v in tag_data:
        if v.type in [1,3]:
            tags['product'].append(v)
        if v.type in [2,3]:
            tags['article'].append(v)
    # 生成页面二维码
    try:
        active_url = request.url
        url_code = set_qrcode(active_url)
    except Exception as err:
            print(err)

    data = dict(
        webconfig = webconfig,
        columns = columns,
        ad_data = ad_data,
        top_nav = top_nav,
        active_nav = active_nav,
        tags = tags,
        url_code = url_code
    )
    return data


@home.route("/click_count", methods=['GET'])
def click_count():
    if ('url' in request.args) and (request.args['url']):
        url = request.args['url']
        if url in CLICKS_COUNT:
            CLICKS_COUNT[url] += 1
        else:
            CLICKS_COUNT[url] = 0
    return 'count+1'
