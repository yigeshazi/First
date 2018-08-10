#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from repository import models


class ArticleForm(django_forms.Form):
    title = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'}),
        error_messages={'required': '标题不能为空',
                        }
    )
    summary = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'}),
        error_messages={'required': '简介不能为空',
                        }
    )
    content = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content','placeholder':'文章内容'}),
        error_messages={'required': '内容不能为空',
                        }
    )
    article_type_id = django_fields.IntegerField(
        widget=django_widgets.RadioSelect(choices=models.Article.type_choices),
        error_messages={'required': '请选择文章类型',
                        }
    )
    category_id = django_fields.ChoiceField(
        choices=[],
        widget=django_widgets.RadioSelect,
        error_messages={'required': '请先添加分类信息',
                        }
    )

    tags = django_fields.MultipleChoiceField(
        choices=[],
        widget=django_widgets.CheckboxSelectMultiple,
        error_messages={'required': '请先添加标签信息',
                        }
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['category_id'].choices = models.Category.objects.filter(blog_id=blog_id).values_list('nid',
                                                                                                         'title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid', 'title')

