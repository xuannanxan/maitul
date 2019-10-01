# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-03-24.
__author__ = 'Allen xu'
from flask import render_template, request,jsonify,session
from app.expand.mail import MailObj,send_email
from app.expand.utils import Pagination
from app.home.forms import MessageForm
from app.models import Crud, Category,Message
from . import home,seoData,cache,getTag,getWebTemplate

@home.route("/search", methods=['GET'])
def search():
    page,tag,search,cate,templates = 1,'','','',[]
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('tag'):
        tag = int(request.args.get('tag'))    
    if request.args.get('cate'):
        cate = int(request.args.get('cate'))    
    if request.args.get('query'):
        search = str(request.args.get('query'))  
    temp_data = {
            "temp": {"template":'search_results'},
            "data": {
                "search_data":searchData(cate,tag,search,page),
                "tags":getTag()
                }
        }
    templates.append(temp_data)
    return render_template("home/%s/home.html"%getWebTemplate(),
            seo_data = seoData(search,search,search) ,
            templates = templates,
            param = {
            'nav_data':'',
            'cate_data':'',
            'content_data':'',
            'tag':tag,
            'cate':cate,
            'search':search
            } 
            ) 

@home.route("/message", methods=['POST'])
def message():
    if request.method == 'POST':
        data = request.form
        form = MessageForm(data)
        ip = request.remote_addr
        # request 数据转为dict
        dict_data = data.to_dict()
        dict_data['ip'] = ip
        if form.validate():
            message_data = Crud.add(Message,dict_data)
            if message_data:
                session['user_email'] = message_data.email
                re_mail = MailObj()
                re_mail.recipients.append(message_data.email)
                send_email(re_mail)
                warn_mail = MailObj()
                warn_mail.subject = '您有新的询盘，请注意查收！'
                warn_mail.html_body = '<p>姓名：%s</p>' \
                                    '<p>邮箱：%s</p>' \
                                    '<p>联系方式：%s</p>' \
                                    '<p>留言内容：%s</p>' \
                                    '<p>用户来源：%s</p>'% (message_data.name, message_data.email,message_data.contact,message_data.info,message_data.ip)
                send_email(warn_mail)
                return {"code":1, "msg": "Message submitted successfully, thank you for your support, we will contact you as soon as possible!"}
            return {"code": 0, "msg": 'System error, message submitted failure, please call our phone.'}
        return {"code": 0, "msg": form.get_errors()}



def searchData(cate_id,tag_id,search,page):
    '''
    数据查询
    '''
    cate_select,tag_select = '',''
    if cate_id:
        cate_select = 'AND b.category_id=%d'%(cate_id)
    if tag_id:
        tag_select = 'AND r.tag_id=%d'%(tag_id)
    sql = '''select SQL_CALC_FOUND_ROWS b.* ,c.type,GROUP_CONCAT(r.tag_id SEPARATOR ',') as tags ,c.pid as cate_pid
    FROM
	(select p.id,p.title,p.cover,p.info,p.content,p.click,p.category_id,p.create_time,p.sort,p.is_del
	from product as p  
	union all 
	select a.id,a.title,a.cover,a.info,a.content,a.click,a.category_id,a.create_time,a.sort,a.is_del
	from article  as a) as b
    left join tag_relation as r on b.id = r.relation_id 
    left join category as c on c.id = b.category_id
    WHERE (b.title LIKE '%{0}%' OR b.content LIKE '%{0}%' OR b.info LIKE '%{0}%' ) {1} {2}
    GROUP BY b.id
    ORDER BY b.sort DESC
    LIMIT {3},{4};
    '''.format(search,tag_select,cate_select,(page-1)*8,8)
    sql_data = Crud.auto_select(sql)
    count_num = Crud.auto_select("SELECT FOUND_ROWS() as countnum")
    count = int((count_num.first()).countnum)
    if sql_data:
        return Pagination(page,8,count,sql_data.fetchall())
    return False
   
