# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.test import TestCase

# Create your tests here.

import requests

response = ''''''# print response


def testjson():
    import json as jjj

    data1 = {'b': 789, 'c': 456, 'a': 123}
    print data1
    encode_json = jjj.dumps(data1)
    # print type(encode_json), encode_json

    # decode_json = json.loads(encode_json)
    # print type(decode_json)
    # print decode_json['a']
    # print decode_json

def transjson():
    decode_json = json.loads(response)
    print type(decode_json)
    page_list = decode_json['data']['pageList']
    page_nums = len(page_list)
    print '元素数量=' + str(page_nums)
    payment_amount = 0
    for i in range(page_nums):
        a = page_list[i]['paymentAmount']
        payment_amount += a

    # print page_list[0]['paymentAmount']
    print payment_amount
#
def test_re():
    import re
    # s = "adfad asdfasdf asdfas asdfawef asd adsfas "
    # re1 = re.compile(r'((\w+)\s+\w+)')
    # '''
    # 把这个按re1按顺序匹配,如果有分组,
    # 从头开始匹配，找到符合re1的放进一个tuple,再往下找，找到再放进一个tuple
    # 再把所有的tuple放进一个lisst
    # '''
    s2 = "[]"
    # re2 = re.compile(r'^\[(\d):(\d)\]$')
    re2 = re.compile(r'^\[([\d]{0,2}):([\d]{0,3})\]$')
    res2 = re2.findall(s2)
    print(res2)

    s3 = "[12333,2,0888,]"
    # re3 = re.compile(r'(\d{0,3}?!\d{3})')
    # re3 = re.compile(r'(\d{1,3}[\,\d[^]]?)')
    # re3 = re.compile(r'(\d{1,3}\,?|[^\d])')
    re3 = re.compile(r'(\d{1,10})')
    # re3 = re.compile(r'[^\d]')
    # re3 = re.compile(r'[^\d](\d{1,5})[^\d]')
    res3 = re3.findall(s3)
    print(res3)

def findall():
    import re

    str = 'xiaohong loves xiaoming,xiaozhu loves xiaoli,xiaopeng loves xiaozhao'

    names = re.findall(r'(\S+) loves (\S+)(,|$)', str, re.I)
    print names
    if names:
        for group in names:
            print group[0], group[1]
def to_sigle_list(datas):
    '''
    把嵌套list数据都放到一个list中
    :param datas:
    :return:
    '''
    l = []
    for data in datas:
        if isinstance(data, list):
            for d in data:
                l.append(d)
        else:
            l.append(data)
    return l
def find(e):
    return '#'

def get_sum_str_exp(express):
    temp = express
    operator_index_list = []
    for i, c in enumerate(express):
        if c in ('+', '-'):
            operator_index_list.append(i)
            temp = temp.replace(c, '*')
    exps = temp.split('*')
    i = 1
    #执行find
    for o_index in operator_index_list:
        exps.insert(i, express[o_index])
        i += 2
    return ''.join(exps)

if __name__ == "__main__":
    a = reduce(lambda x, y: x+y, range(1,101))
    sum([1,2])
    print a
    # a = "b=0.01+0.01"
    # exec(a)
    # print b

    # print to_sigle_list([[1],[2,3],[4,{'a':1}]])

    # print a

    # url = "http://retail.console.saas.weimobqa.com/api3/ec/mgr/b2cOrder/queryOrderList"
    # body = {u'pageNum': 1, u'storeId': 1180222, u'pid': u'1122', u'pageSize': 20,
    #  u'queryParameter': {u'orderStatuses': None, u'createStartTime': 1510457603000L, u'channelTypes': None,
    #                      u'createEndTime': 1513049603849L, u'paymentMethods': None, u'paymentTypes': None,
    #                      u'flagRanks': None, u'bizTypes': None, u'deliveryTypes': None}}
    # # d_result = json.dumps(result)
    # headers = {'Origin': 'http//retail.console.saas.weimobqa.com', 'Content-Length': '276', 'Accept-Language': 'zh-CN,zh;q=0.8,da;q=0.6', 'Accept-Encoding': 'gzip, deflate', 'Apiclient': 'saas-pc', 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'weimob-pid': '1122', 'Host': 'retail.console.saas.weimobqa.com', 'Referer': 'http//retail.console.saas.weimobqa.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Bearer 99707582ada3eaf7da603ccde6f94dfaead537f814533d729f91aeb81a4dec7c'}
    # import requests
    # resp = requests.post(url, json=body, headers=headers)
    # # requests.po
    # print resp.text

