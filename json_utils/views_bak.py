# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.
# 引入我们创建的表单类
from jsontest.data_exec import JsonObj
from .forms import AddForm
from .forms import Register
from django.http import HttpResponse
from jsontest import data_exec
from jsontest import utils
import json
import logging

def index(request):
    if request.method == 'POST':  # 当提交表单时
        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法

            url = form.cleaned_data['url']
            body = form.cleaned_data['body']
            headers = form.cleaned_data['headers']
            response = form.cleaned_data['response']
            request_method = form.cleaned_data['request_method']
            result = {'res': 'sssssssssssssssssssssssssss'}
            # if request_method == 'POST':
            #     result = {'res':'sssssssssssssssssssssssssss'}
            #     pass

            return render(request, 'json_utils/index.html', {'form': form})
            #return HttpResponse(url + " " + body + ' ' + request_method)
    else:  # 当正常访问时
        form = AddForm()
        return render(request, 'json_utils/index.html', {'form': form})

def register(request):
    if request.method == 'POST':
        regform = Register(request.POST, auto_id="%s", error_class=DivErrorList)

        if regform.is_vaild():
            nickname = regform.cleaned_data['nickname'] #别名
            #print nickname
            return HttpResponse(u"{0},欢迎您!".format(nickname))
    else:
        regform = Register(auto_id="%s", label_suffix=":")
        return render(request, "json_utils/register.html", {'reg':regform})

def ajax_aubmit(request):
    print request.POST
    return render(request, 'json_utils/test_ajax.html')

def add(request):
    # return render_to_response(request, 'json_utils/ajax_demo3.html')
    # context_instance = RequestContext(request)
    return render(request, 'json_utils/ajax_demo3.html')

def plus(request):
    reqmethod = request.POST.get('reqmethod', '0').encode('utf-8')
    url = request.POST.get('url', '').encode('utf-8')
    body = request.POST.get('body', '').encode('utf-8')
    headers = request.POST.get('headers', '').encode('utf-8')
    expressions = request.POST.get('expressions', '').encode('utf-8').strip()
    body_param = request.POST.get('body_param', '').encode('utf-8').strip()

    json_path = request.POST.get('json_path', '').encode('utf-8')

    responses, returncode = data_exec.run(url, body, reqmethod, headers, json_path, expressions, body_param)
    response = ''

    #方法1：可以美化显示但是每组数据都由[]包裹
    for i, resp in enumerate(responses):
        if i == 0:
            response = resp
        else:
            response = response + '\n' + resp

    #方法2: 可以去掉[]但是不能那个
    #response = str(responses)

    #我的想法是返回一个然后美化前的list,然后再这里统一美化，顺便把美化前的数据以json 返回出去
    pretty_body = ''
    if body != '':
        try:
            d_body = JsonObj.str2dict(body)
            pretty_body = utils.pretty_dict2(d_body)
        except:
            pretty_body = "body格式错误!"
            returncode = -1
    result = {'response': response, 'body': pretty_body, 'returncode': returncode}
    d_result = json.dumps(result)
    return HttpResponse(d_result)

def count(request):
    request = request.POST.get('res', '0').encode('utf-8')
    d_result = json.dumps({'aa': 123})
    return HttpResponse(d_result)

def pretty_body(request):
    body = request.POST['body'].encode('utf-8')
    d_body = JsonObj.str2dict(body)
    return [utils.pretty_dict2(d_body), 'aaaaaaaaaaaa']