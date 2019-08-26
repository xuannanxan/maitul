# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-03-24.
__author__ = 'Allen xu'
from flask import render_template, request,jsonify
from app.expand.mail import MailObj,send_email
from app.home.forms import MessageForm
from app.models import Crud, Category,Message
from . import home,seo_data,cache

@home.route("/contact/<int:nav_id>", methods=['GET'])
@home.route("/contact", methods=['GET'])
@cache.memoize(60)
def contact(nav_id=None):
    return render_template('home/contact.html',
                           seo_data =seo_data,
                           )

@home.route("/about/<int:nav_id>", methods=['GET'])
@home.route("/about", methods=['GET'])
@cache.memoize(60)
def about(nav_id=None):
    return render_template('home/about.html',
                           seo_data =seo_data,
                           )

@home.route("/message", methods=['POST'])
def message():
    data = request.form
    form = MessageForm(data)
    ip=request.remote_addr

    if form.validate():
        add = Crud.add(Message,data)
        if add['code']==1:
            re_mail = MailObj()
            re_mail.recipients.append(data['email'])
            send_email(re_mail)
            warn_mail = MailObj()
            warn_mail.subject = '您有新的询盘，请注意查收！'
            warn_mail.html_body = '<p>姓名：%s</p>' \
                                '<p>邮箱：%s</p>' \
                                '<p>联系方式：%s</p>' \
                                '<p>留言内容：%s</p>' \
                                '<p>用户来源：%s</p>'% (data['name'], data['email'],data['contact'],data['info'],ip)
            send_email(warn_mail)
            result = {"code":1, "msg": "Message submitted successfully, thank you for your support, we will contact you as soon as possible!"}
        else:
            result = {"code": 2, "msg": 'System error, message submitted failure, please call our phone.'}
    else:
        result = {"code": 2, "msg": form.get_errors()}
    return jsonify(result)
