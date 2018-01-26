# -*- coding: utf8 -*-
__author__ = 'Alex.xu'
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import Queue

class AddForm(forms.Form):
    # a = forms.ModelChoiceField(label=u'队列', queryset=Queue.objects.all())
    request_method = forms.ChoiceField(label=u'Region', choices=(('post', 'POST'), ('get', 'GET')))
    url = forms.CharField(required=False)
    body = forms.CharField(required=False)
    headers = forms.CharField(required=False)
    # response = forms.Textarea()
    response = forms.CharField(required=False)
    # response = forms.CharField(widget=forms.TextArea, required=False)
    # response = forms.CharField(required=False, max_length=254)

SEX_CHOICES = (('male', '男'), ('female', '女'))

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982', '1983', '1984')

class Register(forms.Form):
    nickname = forms.CharField(max_length=20, label="昵称", help_text="请输入您的别名!", widget=forms.TextInput(
        attrs={'class': 'special', 'id': 'nick'}), error_messages={'required': u'别名不能为空'})
    username = forms.CharField(label="用户名", error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=SEX_CHOICES, label="性别")
    email = forms.EmailField(label="邮箱", error_messages={'required': u'邮箱不能为空', 'invalid': u'请输入正确的邮箱'})
    phone = forms.CharField(required=False, label="手机号")
    birthday = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))