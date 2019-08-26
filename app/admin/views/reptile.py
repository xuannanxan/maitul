# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import ReptileForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict,getReptileList,getReptileContent,downImage,full_url,build_tree
from app.models import ReptileRequest,ReptileList,Crud,Category,Article,Product
from .. import admin


# 添加爬虫请求
@admin.route("/reptile/add", methods=["POST"])
@login_required
@auth_required
def reptile_add():
    data = request.form
    form = ReptileForm(data)
    if form.validate():
        result = Crud.add(ReptileRequest,data,"name")
        if result['code'] == 1:
            op_log("添加爬虫请求-%s" % data["name"])
    else:
        result = {"code": 2, "msg": form.get_errors()}
    return jsonify(result)


# 爬虫请求列表
@admin.route("/reptile/request/<int:page>", methods=['GET'])
@admin.route("/reptile/request", methods=['GET'])
@login_required
@auth_required
def reptile_request(page=None):
    page_data = Crud.get_data_paginate(ReptileRequest, ReptileRequest.addtime.desc(), page, 10)
    return render_template("admin/reptile/reptile_request.html", page_data=page_data)

# 已经爬下来的数据
@admin.route("/reptile/list", methods=['GET'])
@login_required
@auth_required
def reptile_list():
    request_id = request.args.get('request_id')
    if request_id:
        request_id = int(request_id)
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1
    request_data = Crud.get_data(ReptileRequest, ReptileRequest.addtime.desc())
    if request_id:
        page_data = Crud.search_data_paginate(ReptileList,ReptileList.request_id==request_id, ReptileList.addtime.desc(), page, 20)
    else:
        page_data = Crud.get_data_paginate(ReptileList, ReptileList.addtime.desc(), page, 20)
    category_data = Crud.get_data(Category,Category.sort.desc())
    category_tree = build_tree(category_data, 0, 0)
    return render_template("admin/reptile/reptile_list.html",
                           request_data = request_data,
                           page_data=page_data,
                           category_tree=category_tree,
                           request_id=request_id)

# 修改爬虫请求
@admin.route("/reptile/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def reptile_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(ReptileRequest, getdata['id'])
        return jsonify({"code": 1, "data": object_to_dict(data)})
    elif request.method == "PUT":
        data = request.form
        form = ReptileForm(data)
        if form.validate():
            result = Crud.update(ReptileRequest,data,"name")
            op_log("修改爬虫请求#%s" %  data["id"])
        else:
            result = {"code": 2, "msg": form.get_errors()}
        return jsonify(result)


# 删除爬虫请求
@admin.route("/reptile/del", methods=['DELETE'])
@login_required
@auth_required
def reptile_del():
    deldata = request.form
    data = ReptileRequest.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    op_log("删除爬虫请求-%s" % data.name)
    return jsonify(result)

    # 开始爬数据
@admin.route("/reptile/get", methods=['GET'])
@login_required
@auth_required
def reptile_get():
    getdata = request.args
    reptile_request = Crud.get_data_by_id(ReptileRequest,getdata['id'])
    urls = []   #处理为数组，接受多页查询
    if reptile_request.begin_page and reptile_request.end_page: #有起止页面
        urls = [reptile_request.url.replace("{}", str(v)) for v in range(int(reptile_request.begin_page),int(reptile_request.end_page)+1)]
    else:
        urls.append(reptile_request.url)
    content_obj = {
        'content_name':reptile_request.content_name,
        'content_info':reptile_request.content_info,
        'content_main':reptile_request.content_main,
        'content_img':reptile_request.content_img,
    }
    page_list,number = [],0
    for url in urls:
        page_list.extend(getReptileList(url,reptile_request.dom))
    for content_url in page_list:
        number+=1
        print('-'*40+'开始爬第%d/%d个数据（%s）'%(number,len(page_list),content_url)+'-'*40)
        #如果url已经被爬过了，跳过
        count = ReptileList.query.filter(ReptileList.is_del == 0,getattr(ReptileList, 'url')==content_url).count()
        if count>0:
            print('-'*40+'该数据已经被拿下'+'-'*40)
            continue
        content = getReptileContent(content_url,content_obj)
        #如果没有取到数据
        if 'content_name'not in content.keys() or 'content_main'not in content.keys():
            return
        #如果有图片，下载图片，替换url
        if 'content_img' in content.keys():
            if content['content_img']:
                content['content_img'] = downImage(full_url(url,content['content_img']))
        content['request_id']=getdata['id']
        content['url']=content_url
        #匹配新增代码，因批量爬取可能会中断，采用采集一个存一个的方式
        # reptile_obj = ReptileList(
        #     request_id=getdata['id'],
        #     url=content_url,
        #     content_name=content['content_name'],
        #     content_info=content.setdefault('content_info', ''),
        #     content_main=content['content_main'],
        #     content_img=content.setdefault('content_img', ''),
        # )
        Crud.add(ReptileList,content,'url')
        print('-'*40+'第%d个数据已爬取成功'%(number)+'-'*40)
    if number>0:
        result={"code": 1, "msg": "已成功爬取"+str(number)+"个数据！"}
    else:
        result = {"code": 2, "msg": "数据不存在或已经被爬过啦！"}
    return  jsonify(result)

# 预览数据
@admin.route("/reptile/preview", methods=['GET'])
@login_required
@auth_required
def reptile_preview():
    getdata = request.args
    data = Crud.get_data_by_id(ReptileList, getdata['id'])
    return jsonify({"code": 1, "data": object_to_dict(data)})

# 删除已爬数据
@admin.route("/reptile/data/del", methods=['DELETE'])
@login_required
@auth_required
def reptile_data_del():
    deldata = request.form
    data = ReptileList.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    op_log("删除爬虫数据-%s" % data.content_name)
    return jsonify(result)

    # 导出数据到栏目
@admin.route("/reptile/export", methods=['PUT'])
@login_required
@auth_required
def reptile_export():
    data = request.form
    #查询全部要到出的数据
    reptile_ids = data['reptile_id'].split(',')
    reptile_data = Crud.search_data(ReptileList,ReptileList.id.in_(reptile_ids))
    #导入到产品
    add_data = []
    if int(data['type'])==1:
        #批量新增
        for v in reptile_data:
            product = Product(
                title=v.content_name,
                cover=v.content_img,
                pictures=v.content_img,
                info=v.content_info,
                content=v.content_main,
                category_id=data['id'],
            )
            add_data.append(product)
    #导入到文章
    elif int(data['type'])==2:
         #批量新增
        for v in reptile_data:
            product = Article(
                title=v.content_name,
                cover=v.content_img,
                info=v.content_info,
                content=v.content_main,
                category_id=data['id'],
            )
            add_data.append(product)
    result = Crud.add_all(add_data)
    return jsonify(result)

