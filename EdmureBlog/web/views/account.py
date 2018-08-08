#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from io import BytesIO
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from utils.check_code import create_validate_code
from repository import models
from ..forms.account import LoginForm,RegisterForm
from django.db.models import Q




def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        message = {'status': False, 'error': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid', 'nickname',
                       'username', 'email',
                       'avatar',
                       'blog__nid',
                       'blog__site',
                       'blog__theme').first()

            if not user_info:
                # result['message'] = {'__all__': '用户名或密码错误'}
                message['error'] = '用户名或密码错误'

            else:
                message['status'] = True
                request.session['user_info'] = user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 30)

        else:
            if 'username' in form.errors:
                message['error'] = form.errors['username']
            if 'password' in form.errors:
                    message['error'] = form.errors['password']

        # else:
        #     print(form.errors)
        #     if 'check_code' in form.errors:
        #         result['message'] = '验证码错误或者过期'
        #     else:
        #         result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(message))


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method=="GET":
        return render(request, 'register.html')
    elif request.method=="POST":
        form = RegisterForm(request=request,data=request.POST)
        message = {'status': False, 'error': None}
        result = form.is_valid()
        if result:
            username = request.POST.get('username')
            email = request.POST.get('email')
            user_obj = models.UserInfo.objects.filter(Q(username=username)| Q(email=email)).first()
            if user_obj:
                message['error'] = '用户名或邮箱已经注册过'
            else:
                form.cleaned_data.pop('confirm_password')
                # form.cleaned_data.pop('check_code')
                print(form.cleaned_data)
                models.UserInfo.objects.create(**form.cleaned_data)
                user_dict = models.UserInfo.objects.filter(username=username).values('nid', 'username', 'email').first()
                # print(type(user_dict))
                request.session['user_info'] = user_dict
                message['status'] = True
        else:
            # print(form.errors)
            if 'username' in form.errors:  # 按照顺序进行验证，先用户名、邮箱、密码、确实密码、密码一致、验证码，用户名邮箱唯一
                message['error'] = form.errors['username']
            else:
                if 'email' in form.errors:
                    message['error'] = form.errors['email']
                else:
                    if 'password' in form.errors:
                        message['error'] = form.errors['password']
                    else:
                        if 'confirm_password' in form.errors:
                            message['error'] = form.errors['confirm_password']
                        else:
                            if '__all__' in form.errors: #整体错误信息/多个错误信息
                                message['error'] = form.errors['__all__']
                            # else:
                            #     if 'check_code' in form.errors:
                            #         message['error'] = form.errors['check_code']
        return HttpResponse(json.dumps(message))

def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()

    return redirect('/')

def xiaoyun(request):
    if request.method == "GET":
        return render(request,'xiaoyun.html')
    else:
        input_code = request.POST.get('code')
        check_cd = request.session['check_code']
        print(input_code,check_cd)
        return HttpResponse('...')

def shizhengwen(request):
    # f = open('static/imgs/avatar/20130809170025.png','rb')
    # data = f.read()
    # f.close()
    f = BytesIO()
    img, code = create_validate_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    # request.session['CheckCode'] = code
    return HttpResponse(f.getvalue())


    # stream = BytesIO()
    # img, code = create_validate_code()
    # img.save(stream, 'PNG')
    # request.session['CheckCode'] = code
    # return HttpResponse(stream.getvalue())


def cunzhang(request):
    return render(request,'cunzhang.html')

def laocunzhang(request):
    ret = {'status': '','msg': ""}
    print(request.POST)
    print(request.FILES)
    dic = {
        'error': 0,
        'url': '/static/imgs/4.jpg',
        'message': '错误了...'
    }

    return JsonResponse(dic)


def find_pwd(request):
    return render(request,'find_pwd.html')
