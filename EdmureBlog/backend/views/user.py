#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import uuid
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse
from ..forms.article import ArticleForm
from ..auth.auth import check_login
from repository import models
from utils.pagination import Pagination
from utils.xss import XSSFilter

@check_login
def index(request):
    return render(request, 'backend_index.html')

@check_login
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    if request.method=='GET':
        blogTheme = [
            {'id': '0', 'name': '默认主题'},
            {'id': '1', 'name': '黑不溜秋'},
            {'id': '2', 'name': '乌七八啦'},
            {'id': '3', 'name': '红色火焰'},
            {'id': '4', 'name': '哈哈哈嘿哈'},
        ]
        return render(request, 'backend_base_info.html',{'blogTheme':blogTheme})

    if request.method=='POST':
        message = {'status': False, 'error': None}
        site = request.session['user_info'].get('blog__site')
        if site:
            nickname = request.POST.get('nickname')
            theme = request.POST.get('theme')
            title = request.POST.get('title') if request.POST.get('title') else None
            user_info_dict = request.session['user_info']
            models.Blog.objects.filter(site=site).update(theme=theme, title=title)
            models.UserInfo.objects.filter(nid=user_info_dict['nid']).update(nickname=nickname)
            user_info_dict['nickname'] = nickname
            user_info_dict['blog__theme'] = theme
            user_info_dict['blog__title'] = title
            request.session['user_info'] = request.session['user_info']
            message['status']=True

        else:
            site=request.POST.get('site')
            if site:
                blog_obj = models.Blog.objects.filter(site=site).first()
                if blog_obj:
                    message['error'] = '博客地址已被占用'
                else:
                    nickname = request.POST.get('nickname')
                    theme = request.POST.get('theme')
                    title = request.POST.get('title')

                    models.Blog.objects.create(site=site,
                                               theme=theme,
                                               title=title,
                                               user_id=request.session['user_info']['nid'])
                    models.UserInfo.objects.filter(nid=request.session['user_info']['nid']).update(nickname=nickname)
                    bid=models.Blog.objects.get(site=site).nid
                    user_info_dict = request.session['user_info']
                    user_info_dict['blog__nid'] = bid
                    user_info_dict['nickname'] = nickname
                    user_info_dict['blog__theme'] = theme
                    user_info_dict['blog__title'] = title
                    user_info_dict['blog__site'] = site
                    print(user_info_dict, request.session['user_info'])
                    request.session['user_info'] = user_info_dict
                    message['status'] = True
            else:
                message['error'] = '博客地址不能为空'

        return HttpResponse(json.dumps(message))

@check_login
def upload_avatar(request):
    message = {'status': False, 'data': None}
    if request.method == 'POST':
        files = request.FILES.get('avatar_img')
        if files:  # 省略判断文件格式的过程
            img_dir = 'static/imgs/savatar/%s' % (request.session['user_info']['username'])
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            img_path = os.path.join(img_dir, 'avatar.png')
            print(img_path)

            with open(img_path, 'wb') as f:
                for item in files.chunks():
                    f.write(item)

            models.UserInfo.objects.filter(nid=request.session['user_info']['nid']).update(avatar=img_path)
            user_info_dict = request.session['user_info']
            user_info_dict['avatar'] = img_path
            request.session['user_info'] = user_info_dict
            print(request.session['user_info'])
            message['data'] = img_path
            message['status'] = True
    return HttpResponse(json.dumps(message))

@check_login
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    if request.method=='GET':
        blog_id = request.session['user_info']['blog__nid']
        tag_list=models.Tag.objects.filter(blog_id=blog_id)
        return render(request, 'backend_tag.html',{'tag_list':tag_list})
    elif request.method=='POST':
        try:
            blog_id = request.session.get('user_info')['blog__nid']
            # print(blog_id) 创建博客后点击添加标签，但是从session重获取不到blog__nid
            tag_name=request.POST.get('tag_name')
            models.Tag.objects.create(title=tag_name, blog_id=blog_id)
            return redirect('/backend/tag.html')
        except Exception:
            return HttpResponse('请先创建博客')

@check_login
def delete_tag(request):
    message={'status':False,'msg':None}
    try:
        nid=request.GET.get('nid')
        models.Tag.objects.filter(nid=nid).delete()
        message['status']=True
    except Exception as e:
        message['msg']='删除失败，请检查该标签下是否还有文章'
    return HttpResponse(json.dumps(message))

@check_login
def edit_tag(request):
    message = {'status': False}
    try:
        nid = request.POST.get('nid')
        title = request.POST.get('title')
        models.Tag.objects.filter(nid=nid).update(title=title)
        message['status'] = True
    except Exception as e:
        message['status'] = str(e)

    return HttpResponse(json.dumps(message))

@check_login
def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    if request.method=="GET":
        blog_nid=request.session.get('user_info')['blog__nid']
        cate_list=models.Category.objects.filter(blog_id=blog_nid)
        # for cate in cate_list:
        #     article_list=cate.article_set.all().values_list('nid')
        #     ids=list(zip(*article_list))[0] if list(zip(*article_list)) else []
        #     cate.__setattr__('count_article',len(ids))
        return render(request, 'backend_category.html',{'cate_list':cate_list})
    elif request.method=="POST":
        blog_id = request.session.get('user_info')['blog__nid']
        cate_name = request.POST.get('cate_name')

        models.Category.objects.create(title=cate_name, blog_id=blog_id)
        return redirect('/backend/category.html')

@check_login
def delete_category(request):
    message={'status':True,'msg':None}
    try:
        nid=request.GET.get('nid')
        models.Category.objects.filter(nid=nid).delete()
        message['msg']='删除成功'
    except Exception as e:
        message['status']=False
        message['msg']='删除失败，请检查该分类下是否还有文章'
    return HttpResponse(json.dumps(message))

@check_login
def edit_category(request):
    message={'status':False}
    try:
        nid=request.POST.get('nid')
        title=request.POST.get('title')
        models.Category.objects.filter(nid=nid).update(title=title)
        message['status']=True

    except Exception as e:
        message['status']=str(e)

    return HttpResponse(json.dumps(message))

@check_login
def article(request, *args, **kwargs):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    blog_id = request.session['user_info']['blog__nid']
    condition = {}
    for k, v in kwargs.items():
        if v == '0':
            pass
        else:
            condition[k] = v
    condition['blog_id'] = blog_id
    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p', 1), data_count)
    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title','blog').select_related('blog')[page.start:page.end]
    page_str = page.page_str(reverse('article', kwargs=kwargs))
    category_list = models.Category.objects.filter(blog_id=blog_id).values('nid', 'title')
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices)
    kwargs['p'] = page.current_page
    return render(request,
                  'backend_article.html',
                  {'result': result,
                   'page_str': page_str,
                   'category_list': category_list,
                   'type_list': type_list,
                   'arg_dict': kwargs,
                   'data_count': data_count
                   }
                  )

@check_login
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ArticleForm(request=request)
        return render(request, 'backend_add_article.html', {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                tags = form.cleaned_data.pop('tags') # 移出 tags需要在第三张Article2Tag表上手动添加
                content = form.cleaned_data.pop('content')# 移出 content需要在表ArticleDetail上手动添加、关联Article
                content = XSSFilter().process(content) # 对content进行数据过滤  过滤掉script等标签
                form.cleaned_data['blog_id'] = request.session['user_info']['blog__nid']# 把博客id添加到cleande_data中
                # dict格式cleaned_data 包含的字段{ 'blog_id' 'article_type' 'category_id'  'summary'  'title'  }
                obj = models.Article.objects.create(**form.cleaned_data) # Article表添加cleaned_data里的内容
                models.ArticleDetail.objects.create(content=content, article=obj) # ArticleDetail添加数据、关联
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)

            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_add_article.html', {'form': form})
    else:
        return redirect('/')

@check_login
def edit_article(request, nid):
    """
    编辑文章
    :param request:
    :return:
    """
    blog_id = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
        if not obj:
            return render(request, 'backend_no_article.html')
        tags = obj.tags.values_list('nid')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'nid': obj.nid,
            'title': obj.title,
            'summary': obj.summary,
            'category_id': obj.category_id,
            'article_type_id': obj.article_type_id,
            'content': obj.articledetail.content,
            'tags': tags
        }
        form = ArticleForm(request=request, data=init_dict)
        return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
            if not obj:
                return render(request, 'backend_no_article.html')
            with transaction.atomic():
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)
                tags = form.cleaned_data.pop('tags') #tags是个列表
                models.Article.objects.filter(nid=obj.nid).update(**form.cleaned_data)
                models.ArticleDetail.objects.filter(article=obj).update(content=content)
                models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})

@check_login
def del_article(request):
    message = {'status': False, 'msg': None}
    try:
        nid = request.GET.get('nid')
        models.Article.objects.filter(nid=nid).delete()
        message['status'] = True
    except Exception as e:
        message['msg'] = '删除失败，请重新再试'
    return HttpResponse(json.dumps(message))