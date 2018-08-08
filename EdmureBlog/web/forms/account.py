#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from django.forms import widgets

from repository import models

from .base import BaseForm


class LoginForm(BaseForm,forms.Form):
    # username = django_fields.CharField(
    # min_length=6,
    # max_length=20,
    #     error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"}
    # )
    username = fields.CharField(
        max_length=24,
        # help_text='用户名必须包含数字、字母、特殊符号，字母区分大小写',
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': "请输入用户名"}),
        error_messages={'required': '用户名不能为空',
                        'max_length': '密码长度不能大于12位'}

    )

    # password = django_fields.RegexField(
    #     '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
    #     min_length=12,
    #     max_length=32,
    #     error_messages={'required': '密码不能为空.',
    #                     'invalid': '密码必须包含数字，字母、特殊字符',
    #                     'min_length': "密码长度不能小于8个字符",
    #                     'max_length': "密码长度不能大于32个字符"}
    # )
    password = fields.CharField(
        max_length=12,
        # min_length=6,
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}),
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6位',
                        'max_length': '密码长度不能大于12位'}
    )
    rmb = fields.IntegerField(required=False)

    # check_code = django_fields.CharField(
    #     error_messages={'required': '验证码不能为空.'}
    # )

    # def clean_check_code(self):
    #     if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
    #         raise ValidationError(message='验证码错误', code='invalid')


class RegisterForm(BaseForm,forms.Form):
    username = fields.CharField(
        max_length=24,
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': "请输入用户名"}),
        error_messages={'required': '用户名不能为空',
                        'max_length': '用户名长度不能大于24位'}
    )

    email = fields.EmailField(
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': "请输入邮箱"}),
        error_messages={'required': '邮箱不能为空', 'invalid':'邮箱格式不正确'}
    )

    password = fields.CharField(
        max_length=12,
        # min_length=6,
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}),
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6位',
                        'max_length': '密码长度不能大于12位'}
    )

    confirm_password = fields.CharField(
        max_length=12,
        # min_length=6,
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请重新输入密码"}),
        error_messages={'required': '确认密码不能为空', 'min_length': '确认密码长度不能小于6位',
                        'max_length': '密码长度不能大于12位'}
    )

    nickname = fields.CharField(
        max_length=24,
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': "请输入昵称"}),
        error_messages={'required': '昵称不能为空',
                        'max_length': '昵称长度不能大于24位'}
    )
    # check_code = fields.CharField(
    #     error_messages={'required': '验证码不能为空',}
    # )

    # def clean_check_code(self):
    #     print(self.request.POST.get('check_code').upper())
    #     print(self.request.session['CheckCode'].upper())
    #     if self.request.POST.get('check_code').upper() == self.request.session['CheckCode'].upper():
    #         return self.cleaned_data['check_code']
    #     else:
    #         raise ValidationError(message='验证码错误')

    def clean(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password == password:
            return self.cleaned_data
        else:
            raise ValidationError(message='两次密码输入的不一致')


    # def __init__(self, request, *args, **kwargs):
    #     self.request = request
    #     super().__init__(*args, **kwargs)




