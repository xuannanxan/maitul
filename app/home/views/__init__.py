# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.

from flask import request,current_app,session
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
            return getTopColumn(data,v.pid)
        return

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
    #当前页面的最上级栏目
    top_nav = session.get('top_nav')
    active_nav = session.get('active_nav')
    # 生成页面二维码
    try:
        active_url = request.url
        url_code = set_qrcode(active_url)
    except Exception as err:
            print(err)
    
    data = dict(
        navs = getNavs(),
        webconfig = getWebConfig(),
        top_nav = top_nav,
        active_nav = active_nav,
        url_code = url_code
    )
    return data

# 点击数计算
@home.route("/click_count", methods=['GET'])
def click_count():
    if ('url' in request.args) and (request.args['url']):
        url = request.args['url']
        if url in CLICKS_COUNT:
            CLICKS_COUNT[url] += 1
        else:
            CLICKS_COUNT[url] = 0
    return 'count+1'


# 获取站点配置信息
@cache.cached(timeout=600, key_prefix='webconfig')
def getWebConfig():
    webconfig = {}
    conf_model_data = Crud.get_data(Conf,Conf.sort.desc())
    for v in conf_model_data:
        webconfig[v.ename] = v.default_value
    return webconfig


# 获取菜单
@cache.cached(timeout=600, key_prefix='navs')
def getNavs():
    category_data = getCategory()
    navs_data = [v for v in category_data if v.is_nav == 1]
    navs = build_tree(navs_data, 0, 0)
    return navs


# 获取全部栏目
@cache.cached(timeout=600, key_prefix='category')
def getCategory():
    category_data = Crud.get_data(Category,Category.sort.desc())
    return category_data


# 获取网站模板
@cache.cached(timeout=600, key_prefix='template')
def getTemplate():
    webconfig = getWebConfig()
    template = 'default'
    if 'templates' in webconfig:
        if webconfig['templates']:
            template = webconfig['templates']
    return template