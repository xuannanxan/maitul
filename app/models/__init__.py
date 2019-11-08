# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from app.models.role import Role,Auth
from app.models.log import Adminlog,Operationlog,Userlog
from app.models.base import Crud,and_,or_,not_
from app.models.category import Category
from app.models.article import Article
from app.models.product import Product
from app.models.tag import Tag,TagRelation
from app.models.ad import Ad,Adspace
from app.models.admin import Admin
from app.models.user import User
from app.models.menu import Menu
from app.models.conf import Conf
from app.models.reptile import ReptileRequest,ReptileList
from app.models.message import Message
from app.models.favorite import Favorite
from app.models.footmark import Footmark
from app.models.template import Template
Admin = Admin
Role = Role
Auth =Auth
Crud = Crud
Adminlog = Adminlog
Operationlog =Operationlog
Tag =Tag
Article = Article
Product = Product
Message = Message
Favorite = Favorite
Footmark = Footmark
Category = Category
Userlog = Userlog
Ad = Ad
Adspace = Adspace
Menu = Menu
Conf = Conf
ReptileRequest=ReptileRequest
ReptileList=ReptileList
TagRelation =TagRelation
Template = Template
User = User
and_ = and_
or_ = or_
not_ = not_