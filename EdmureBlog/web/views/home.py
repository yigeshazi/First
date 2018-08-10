#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from repository import models
from utils.pagination import Pagination
from django.urls import reverse

def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """
    # return render(request,'index.html')
    # 获取文章类型
    article_type_list = models.Article.type_choices
    # {},[]
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs=kwargs)#   all/1.html
    else:
        article_type_id = None
        base_url = '/' # /

    data_count = models.Article.objects.filter(**kwargs).count()

    page_obj = Pagination(request.GET.get('p'),data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    article_list_by_comment=models.Article.objects.filter(**kwargs).order_by('-comment_count')
    page_str = page_obj.page_str(base_url)

    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'page_str': page_str,
        }
    )

def home(request, site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    # tag_list = models.Tag.objects.filter(blog_id=blog.nid)
    category_list = models.Category.objects.filter(blog=blog)


    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    article_list = models.Article.objects.filter(blog=blog).order_by('-nid').all()

    return render(
        request,
        'home.html',
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )

def filter(request, site, condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    template_name = "home_summary_list.html"
    if condition == 'tag':
        template_name = "home_title_list.html"
        article_list = models.Article.objects.filter(tags=val, blog=blog).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(category_id=val, blog=blog).all()
    elif condition == 'date':
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
        # select * from tb where blog_id=1 and strftime("%Y-%m",create_time)=2017-01
    else:
        article_list = []

    return render(
        request,
        template_name,
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )

from django.utils.safestring import mark_safe
def detail(request, site, nid):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog_obj = models.Blog.objects.filter(site=site).prefetch_related('user').first()  # 当前用户对应的博客对象
    user_obj = blog_obj.user
    # print(user_obj)
    article_obj = models.Article.objects.filter(nid=nid, blog=blog_obj).first()  # 当前访问的文章对象
    content_obj = models.Comment.objects.filter(article=article_obj)

    if article_obj:
        detail_obj = models.ArticleDetail.objects.filter(article=article_obj).first()  # 访问文章的内容
        content = mark_safe(detail_obj.content)  # 标记安全
        return render(request, 'home_detail.html', {'article_obj': article_obj,
                                                    'content': content,
                                                    'user_obj': user_obj,
                                                    'blog_obj': blog_obj,
                                                    'content_obj': content_obj})
    else:

        return HttpResponse('文章不存在')

import json
def update_comment(request):
    data = {'status':True,'message':None}
    user_id = request.session['user_info']['nid']
    print(user_id)
    if request.method == 'POST':
        print(request.POST)
        content = request.POST.get('content')
        article_id = request.POST.get('article_id')
        reply_id = request.POST.get('reply_id')
        nickname, new_content = content_handle(content)

        if reply_id:
            comment_obj = models.Comment.objects.filter(article_id=article_id,nid=reply_id).first()
            models.Comment.objects.create(user_id=user_id, content=new_content, article_id=article_id,reply=comment_obj)

        else:
            models.Comment.objects.create(user_id=user_id, content=content, article_id=article_id)
            models.Article.objects.filter(nid=article_id).update(comment_count=F("comment_count") + 1)
    return HttpResponse(json.dumps(data))

import re

def content_handle(content):            #对评论内容进行处理
    obj = re.match('@.+\s', content)
    if obj:
        print(obj.group())
        nickname = re.sub('@', '', obj.group()).strip()     # 用户名
        print(nickname)
        new_content = content.split(nickname)[1].strip()    # 评论内容
        print(new_content)
    else:
        nickname = None
        new_content = content
    return nickname,new_content

def up_down(request):
    message = {"status": False,'msg':None}
    article_id = request.POST.get("aid")
    user_id = request.session['user_info']['nid']
    is_up = request.POST.get("is_up")
    is_up=json.loads(is_up)
    print(article_id,user_id,is_up)
    obj=models.UpDown.objects.filter(article_id=article_id,user_id=user_id).first()
    if obj:#不是第一次对文章进行点赞或取消点赞操作，即数据库中已有记录
        if obj.up:
            obj.up=False
            obj.save()
            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") - 1)

        else:
            obj.up=True
            obj.save()
            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
            message['status'] = True
    else:#第一次对文章点赞
        models.UpDown.objects.create(article_id=article_id,user_id=user_id,up=is_up)
        models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
        message['status'] = True

    return HttpResponse(json.dumps(message))
    # try:
    #     up=models.UpDown.objects.filter(article_id=article_id,user_id=user_id).values('up')
    #     if up:
    #         models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") - 1)
    #         models.UpDown.objects.filter(user_id=user_id, article_id=article_id).update(up=False)
    #         response['status']=False
    #     else:
    #         models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=is_up)
    #         models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
    #
    # except Exception as e:
    #     pass
