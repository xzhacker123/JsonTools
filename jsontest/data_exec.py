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
    def get_json(json_dict, json_path, condition=[]):
        jsonpath_expr = parse(json_path)
        male = jsonpath_expr.find(json_dict)
        data = [match.value for match in male]
        new_data = []
        EXPRESS = ['==', '!=', '<=', '>=', '>', '<']
        for d_temp in data:
            # d = unicode_dict_list_to_str(d_temp)
            d = d_temp
            temp = 0
            for i in condition:
                for e in EXPRESS:
                    flag = False
                    if e in i and e + '=' not in i:
                        k, v = i.split(e)
                        # 执行条件筛选
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
                            # 条件有几个temp就加几次,temp数(符合条件数)和条件数相等才能添加到new_data里面
                            temp += 1
                            break
                if not flag:
                    break
                    # 如果连之前的条件都不满足就没有必要再比下去了直接break

            if temp == len(condition):
                new_data.append(d)
        return new_data
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

def get_count(data, express):
    index = []
    all_data = []
    normal_exp, dis_exp = get_all_express(express)
    #暂时只支持单筛选条件
    if len(normal_exp) > 1:
        return "暂不支持多条件筛选!"
    for i, d in enumerate(data):
        for e in dis_exp:
            j = JsonObj.get_json(d, e)
            if len(j) == 1:
                if j[0] not in all_data:
                    index.append(i) #加入下标
                    all_data.append(j[0])
            elif len(j) > 1:
                return "请选择单一字段去重!"
            elif len(j) == 0:
                return "请根据返回数据填写正确的去重表达式!"
            else:
                return "统计未知异常1!"

    #根据已经去重的列表统计
    count = 0
    returncode = 1
    if normal_exp == [] and dis_exp != []:
        count = len(index)

    elif normal_exp == [] and dis_exp == []:
        count = len(data)
    else:
        if index == []:
            index = [i for i in range(len(data))]
        for i in index:
            try:
                j = JsonObj.get_json(data[i], normal_exp[0]) #只筛选第一个条件
                length = len(j)
                count += length
            except:
                return "统计未知异常2!"

    return count

def get_sum_str_exp(data, express):
    '''
    根据操作符表达式 拼接 求和计算表达式
    :param data:
    :param express:
    :return: str类型求和表达式
    '''
    temp = express
    operator_index_list = []
    #暂时不支持多表达式求和
    for i, c in enumerate(express):
        if c in ('+', '-'):
            operator_index_list.append(i)
            temp = temp.replace(c, '*')
    if '*' in temp:
        exps = temp.split('*')
    else:
        if isinstance(temp, str):   #如果是没有操作符的，就直接转换为一个list
            exps = [temp]

    #执行find
    values = []
    for e in exps:
        value = JsonObj.get_json(data, e)
        ss = 0
        for v in value:
            ss += float(v)
        values.append(str(ss)) #添加第一个查询到的值
    i = 1
    for o_index in operator_index_list:
        values.insert(i, express[o_index])
        i += 2
    return ''.join(values)

def get_sum(data, express):
    index = []
    all_data = []
    normal_exp, dis_exp = get_all_express(express)
    # 暂时只支持单筛选条件

    if len(normal_exp) > 1:
        return "暂不支持多条件筛选!"
    sum = 0
    for i, d in enumerate(data):
        for e in dis_exp:
            j = JsonObj.get_json(d, e)
            if len(j) == 1:
                if j[0] not in all_data:
                    index.append(i)  # 加入下标
                    all_data.append(j[0])
            elif len(j) > 1:
                return "请选择单一字段去重!"
            elif len(j) == 0:
                return "请根据返回数据填写正确的去重表达式!"
            else:
                return "统计未知异常1!"

    # 根据已经去重的列表统计求和
    sum = 0
    returncode = 1
    #如果求和表达式为空的话就直接对列表求和
    if normal_exp == []:
        for i in data:
            try:
                i = float(i)
            except:
                return "列表不支持默认求和!"
            sum += i
    else:
        if index == []:
            index = [i for i in range(len(data))]
        for i in index:
            try:
                #这里的normal_exp[0]要处理一下准备求和
                sum_express = get_sum_str_exp(data[i], normal_exp[0])
                sum_exp = 'sub_sum=%s' % sum_express
                exec(sum_exp)
                sum += float(sub_sum)
            except:
                return "统计未知异常2!"

    return sum

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

def get_distinct_express(express):
    '''
    获取去重json表达式{*}
    :param express: 原始表达式
    :return: 去重jsonPath列表
    '''
    re1 = re.compile(r'^{(.*)}$')
    # express = u"[*].buyerInfo.wid;{[*].buyerInfo.wid}"
    exp = []
    if isinstance(express, (unicode)):
        value = express.encode('utf-8')
    try:
        es = value.split(';')
    except:
        es = []
    for e in es:
        e = e.strip()
        res1 = re1.findall(e)
        if res1 != []:
            for i in res1:
                exp.append(i)
    return exp
def get_sum_express(express):
    '''
    获取求和表达式
    :param express:
    :return:
    '''
    operator = ('+', '-')
    re1 = re.compile(r'^{(.*)}$')
    # express = u"[*].buyerInfo.wid;{[*].buyerInfo.wid}"
    distinct_exp = []
    normal_exp = []
    if isinstance(express, (unicode)):
        value = express.encode('utf-8')
    try:
        es = value.split(';')
    except:
        es = []
    for e in es:
        e = e.strip()
        res1 = re1.findall(e)
        if res1 != []:
            for i in res1:
                distinct_exp.append(i)
        elif e != '':   #如果是正常求和表达式

            normal_exp.append(e)
    return normal_exp, distinct_exp

def get_all_express(express):
    '''
    获取非去重表达式和去重表达式
    :param express:
    :return:
    '''
    re1 = re.compile(r'^{(.*)}$')
    # express = u"[*].buyerInfo.wid;{[*].buyerInfo.wid}"
    distinct_exp = []
    normal_exp = []
    if isinstance(express, (unicode)):
        value = express.encode('utf-8')
    try:
        es = value.split(';')
    except:
        es = []
    for e in es:
        e = e.strip()
        res1 = re1.findall(e)
        if res1 != []:
            for i in res1:
                distinct_exp.append(i)
        elif e != '':
            normal_exp.append(e)
    return normal_exp, distinct_exp

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

def trans_body_param(body, body_param, page_num=100):
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
                re2 = re.compile(r'(\d{1,20})')
                res2 = re2.findall(v)
                if res2 == []:
                    return None
                else:   #[1,2,3,4,...]按指定下标查
                    for i in res2:
                        temp = d_body
                        if isinstance(temp[k], int): #如果是整数类型
                            temp[k] = int(i)
                        elif isinstance(temp[k], float):    #如果是浮点型
                            temp[k] = float(i)
                        else:   #如果是字符串类型
                            temp[k] = str(i)
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
        return ["请输入URL!"], [], -1, 0
    if (body is None or body == '') and (reqmethod == "1") and (body_param is not None or body_param != ''):
        return ["请输入body!"], [], -1, 0

    timestamp = utils.get_nowtime_stamp(is_unix=True)
    bodys = trans_body_param(body, body_param)
    if isinstance(bodys, list):
        req = RequestObj(url, bodys, headers, body_param)
        if reqmethod == "1":
            resps = req.post()
        else:
            resps = req.get()
        find_resps = []
        list_resps = []
        # timestamp = utils.get_nowtime_stamp(is_unix=True)
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
                list_resps.append(list_resp)
            except:
                find_resps.append(resp)

        return find_resps, list_resps, 0, timestamp
    else:
        return bodys, [], -1, timestamp
def trans_times(usual_times, unix_times, timestamp_type=True):
    if usual_times == '' and unix_times == '':
        return json.dumps({'returncode': -1})
    elif unix_times != '' and usual_times == '':
        #unix_times转换成usual_times
        try:
            dt = utils.time_stamp2time(unix_times)
            return json.dumps({'returncode': 2, 'usual_times': dt, 'unix_times': unix_times})
        except:
            return json.dumps({'returncode': -3})   #时间戳格式错误
    else:
        #usual_times转换成unix_times
        try:
            t_stamp = utils.get_time_stamp(usual_times, timestamp_type)
            return json.dumps({'returncode': 1, 'usual_times': usual_times, 'unix_times': t_stamp})
        except:
            return json.dumps({'returncode': -2})   #表示usual时间格式错误

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