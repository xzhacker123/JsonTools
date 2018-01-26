# -*- coding: utf8 -*-
__author__ = 'Alex.xu'

import requests
import json
import re
from jsonpath_rw import jsonpath, parse
from jsontest import utils

class JsonObj(object):
    def __init__(self, json_context):
        self.__json_context = json_context
        self.json_dict = json.loads(json_context)
        #self.str2dict(json_context)

    @staticmethod
    def str2dict(json_context):
        return json.loads(json_context)

    @staticmethod
    def headers2dict(headers):
        '''
        返回header
        :param headers:
        :return:
        '''
        m_header = {}
        headers = headers.strip()
        if headers is not '':
            for i in headers.split('\n'):
                k_v = i.split(': ')
                if len(k_v) == 2:
                    k, v = k_v
                else:
                    k_v = i.split(':')
                    k = k_v[0]
                    v = ""
                    for j in k_v[1:]:
                        v += j
                m_header[k] = v.strip()
        if m_header == {}:
            return None
        else:
            return m_header

    @staticmethod
    def dict2str(json_dict):
        pass

    def sum(self, json_path, condition=[], alias=None):
        '''
        json数据值求和统计
        :param json_context: json文本
        :param json_path:   jsonpaht
        :param condition:   筛选条件
        :param alias:   结果别名
        :return: 求和结果
        '''
        pass

    def count(self, json_context, json_path, condition=[], alias=None):
        '''
        求json节点总数
        :param json_context: json文本
        :param json_path:   jsonpaht
        :param condition:   筛选条件
        :param alias:   结果别名
        :return: 统计结果
        '''
        pass

    @staticmethod
    def find_json(json_dict, json_path, condition=[]):
        '''
        查找符合条件的json列表
        :param json_dict:   json字典结构
        :param json_path:   json_path
        :param condition:   筛选条件 [==|=], !=, >, <, >=, <= ,
        :return:
        '''
        jsonpath_expr = parse(json_path)
        male = jsonpath_expr.find(json_dict)
        data = [match.value for match in male]
        new_data = []
        EXPRESS = ['==', '!=', '<=', '>=', '>', '<']
        for d_temp in data:
            #d = unicode_dict_list_to_str(d_temp)
            d = d_temp
            temp = 0
            for i in condition:
                for e in EXPRESS:
                    flag = False
                    if e in i and e+'=' not in i:
                        k, v = i.split(e)
                        #执行条件筛选
                        if isinstance(d, (dict)):
                            b = d[k]
                            if isinstance(d[k], (unicode)):
                                value = d[k].encode('utf-8')
                                if isinstance(value, basestring):
                                    exec ("if \"%s\" %s %s: flag=True" % (d[k].encode('utf-8'), e, v))
                                else:
                                    exec ("if %s %s %s: flag=True" % (d[k].encode('utf-8'), e, v))
                            else:
                                exec ("if d['%s'] %s %s: flag=True" % (k, e, v))
                        if flag:
                            #条件有几个temp就加几次,temp数(符合条件数)和条件数相等才能添加到new_data里面
                            temp += 1
                            break
                if not flag:
                    break
                #如果连之前的条件都不满足就没有必要再比下去了直接break

            if temp == len(condition):
                new_data.append(d)
        return utils.pretty_dict2(new_data), new_data
        # return new_data

def unicode_dict_list_to_str(d_temp):
    '''
    把list或者dict中的unicode字段转换为str
    :param d_temp:
    :return:
    '''
    if isinstance(d_temp, (dict)):
        d = {}
        # 中文(unicode)转换成str
        for dk, dv in d_temp.items():
            if isinstance(dk, (unicode)):
                dk = dk.encode('utf-8')
            if isinstance(dv, (unicode)):
                dv = dv.encode('utf-8')
            d[dk] = dv
    elif isinstance(d_temp, (list)):
        d = []
        for list_v in d_temp:
            if isinstance(list_v, (unicode)):
                list_v = list_v.encode('utf-8')
            d.append(list_v)
    return d

class RequestObj(object):
    import requests
    def __init__(self, url=None, body=None, header=None, body_param=None):
        self.__url = url
        self.__body = body
        self.__header = JsonObj.headers2dict(header)
        self.__session = requests.session()
        self.__bodys = []
        self.body_param = body_param

    def post(self):
        results = []
        for body in self.__body:
            result = self.__session.post(self.__url, json=body, headers=self.__header)
            results.append(result.text)
        return results

    def get(self):
        result = self.__session.get(self.__url, json=self.__body, headers=self.__header)
        return result.text

def json_path_parse():
    from jsonpath_rw import jsonpath, parse
    json_obj = {"student": [{"male": 176, "female": 162}, {"male": 174, "female": 159}]}
    jsonpath_expr = parse("$.student[*].male")
    male = jsonpath_expr.find(json_obj)
    # print male
    # print [match.value for match in male]

def test(condition):
    for i in condition:
        temp = 0
        for e in EXPRESS:
            if e in i:
                print i.split(e)
                break
            temp += 1
        if temp >= len(EXPRESS):
            raise Exception('条件表达式错误')
'''
reqmethod = request.POST['reqmethod']
    url = request.POST['url']
    body = request.POST['body']
    headers = request.POST['headers']
    expressions = request.POST['expressions']
'''

def trans_body_param(body, body_param, page_num=10):
    '''
    body 参数化
    :param body: body
    :param body_param: body参数化表达式
    :param page_num: 默认页面数
    :return: 返回一个参数化的body list
    '''
    bodys = []
    if body == "" or body == None:
        return bodys
    else:
        try:
            d_body = json.loads(body)
        except:
            return "body形式错误!"
        body_param = body_param.strip()

        #body没有参数化就一个body数据
        if body_param is None or body_param == '':
            bodys.append(d_body)
        else:
            try:
                k, v = body_param.split('=')
            except:
                return "body参数形式错误!"
            re1 = re.compile(r'^\[([\d]{0,2}):([\d]{0,3})\]$')
            res1 = re1.findall(v)
            if res1 == []:
                re2 = re.compile(r'(\d{1,10})')
                res2 = re2.findall(v)
                if res2 == []:
                    return None
                else:   #[1,2,3,4,...]按指定下标查
                    for i in res2:
                        temp = d_body
                        temp[k] = i
                        bodys.append(temp.copy())
            else:   #[1:3]按指定区间查
                # 暂时只接收一层k
                index_1, index_2 = res1[0]
                n, m = 0, 0
                try:
                    if index_1 != '':
                        n = int(index_1)
                        if n > page_num:
                            return "输入页面数%d超出设定值!" % n
                    if index_2 != '':
                        m = int(index_2)
                        if m > page_num:
                            return "输入页面数%d超出设定值!" % m
                except:
                    return "body表达式错误!"

                if index_1 == '' and index_2 != '':  # [:n]
                    for i in range(1, m + 1):
                        temp = d_body
                        temp[k] = i
                        bodys.append(temp.copy())
                elif index_1 != '' and index_2 == '':  # [n:]
                    for i in range(n, page_num + 1):
                        temp = d_body
                        temp[k] = i
                        bodys.append(temp.copy())
                elif index_1 != '' and index_2 != '':  # [n:m]
                    for i in range(n, m + 1):
                        temp = d_body
                        temp[k] = i
                        bodys.append(temp.copy())
                else:
                    for i in range(1, page_num + 1):
                        temp = d_body
                        temp[k] = i
                        bodys.append(temp.copy())
        return bodys

def run(url, body=None, reqmethod="0", headers=None, json_path=None, expressions=None, body_param=None):
    if url is None or url == "":
        return ["请输入URL!"], -1
    if (body is None or body == '') and (reqmethod == "1") and (body_param is not None or body_param != ''):
        return ["请输入body!"], -1

    bodys = trans_body_param(body, body_param)
    if isinstance(bodys, list):
        req = RequestObj(url, bodys, headers, body_param)
        if reqmethod == "1":
            resps = req.post()
        else:
            resps = req.get()
        find_resps = []
        for resp in resps:
            if isinstance(resp, (unicode)):
                # 中文(unicode)转换成str
                resp = resp.encode('utf-8')
            try:
                #如果不是json对象就会抛出转换异常
                json_obj = JsonObj(resp)
                if json_path is None or json_path == "":
                    json_path = "$"
                if expressions is None or expressions == "":
                    condition = []
                else:
                    condition = expressions.split('\n')
                str_resp, list_resp = JsonObj.find_json(json_obj.json_dict, json_path, condition)
                find_resps.append(str_resp)
            except:
                find_resps.append(resp)
        return find_resps, 0
    else:
        return bodys, -1

def main():
    url = r'http://retail.console.saas.weimobqa.com/api3/ec/mgr/b2cOrder/queryOrderList'
    body = r'{"pid":"115","storeId":420115,"pageNum":1,"pageSize":200,"queryParameter":{"searchType":4,"channelTypes":null,"orderStatuses":null,"paymentMethods":null,"paymentTypes":null,"flagRanks":null,"bizTypes":null,"deliveryTypes":null,"createStartTime":1511712000000,"createEndTime":1511884799999}}'
    header = r'''Host: retail.console.saas.weimobqa.com
Connection: keep-alive
Content-Length: 289
Origin: http://retail.console.saas.weimobqa.com
weimob-pid: 115
Authorization: Bearer f96614343213119a91c80b0d6e216814ea097f85a031831a52e50f9bebaad8ab
Content-Type: application/json;charset=UTF-8
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Apiclient: saas-pc
Referer: http://retail.console.saas.weimobqa.com/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8,da;q=0.6
Cookie: rprm_cuid=MTUxMTg1MzcyMTcx; saasAuthData_qa=f96614343213119a91c80b0d6e216814ea097f85a031831a52e50f9bebaad8ab; authDataType_qa=saas; Hm_lvt_c1df8c79ab44a42f4e36f5ae9b1f6d48=1511853744; saas.console.session=s%3Aqxedkcw-pLq_Ho-4gD3Le_1qHJFrgodd.vXL0DBhD6aVizjx0moMsdZtKz9v%2FcpOJ9kjUGwl%2BB%2B8; express.session=s%3AK68uy6qI-ZkePKL8iNU9GfThquJbzAAw.bpI1fBFUgwNRpPZsWxDtAD5OjvJqoRsDgYHsH9vqxTE'''
    # header = r'{}'
    # req = RequestObj(url, body)
    # print req.post()
    # for k, v in m_header.items():
    #     print k+":"+v
    req = RequestObj(url, body, m_header)
    resp = req.post()
    j = JsonObj(resp)

    json_path = '$.data.pageList[:100]'
    condition = ['paymentTypeName=="线上支付"', 'wid==4224731']
    # condition = []
    l = JsonObj.find_json(j.json_dict, json_path, condition)
    print "查询到%s条数据:" % len(l)
    for i in l:
        if i == u"公众号":
            print i
        else:
            print i

    # j = j.
if __name__ == '__main__':
    pass
    # condition = ['sssss>=ssss']
    # test(condition)
    # json_path_parse()

    # exec("if Flase:print 'hahaf' and else:print 'caocoa'")
    # main()
    # print

    # EXPRESS = ['==', '!=', '<=', '>=', '>', '<', '=']
    # for e in EXPRESS:
    #     print e

    # print
    # s="小程序"
    # print type(s)
    # s2 = s.decode('utf-8')
    # print s2
    # print type(s2)
    # s3 = s2.encode('utf-8')
    # print type(s3)
    # print s3
    #
    # if s==s3:
    #     print True
    # if 3> =2:print "hahah"