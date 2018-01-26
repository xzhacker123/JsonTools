# -*- coding: utf8 -*-
__author__ = 'Alex.xu'
import time, datetime
import os
try:
    import cPickle as pickle
except ImportError:
    import pickle

def pretty_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            # 如果是字符串则拼上""
            if isinstance(k, basestring): k = '"%s"' % k
            if isinstance(v, basestring): v = '"%s"' % v
            # 如果是字典则递归
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
            # case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:  # 开头,拼左花括号
                if len(obj) == 1:
                    yield '{%s: %s}' % (k, v)
                else:
                    yield '{%s: %s,\n' % (k, v)
            elif i == len(obj) - 1:  # 结尾,拼右花括号
                yield '%s%s: %s}' % (indent, k, v)
            else:  # 中间
                yield '%s%s: %s,\n' % (indent, k, v)

    return ''.join(_pretty(obj, indent))

def pretty_dict2(obj, indent=' '):
    '''
    比起1来多兼容list
    :param obj:
    :param indent:
    :return:
    '''
    def _pretty(obj, indent):
        if isinstance(obj, (dict)):
            for i, tup in enumerate(obj.items()):
                k, v = tup
                # 如果是字符串则拼上""
                if isinstance(k, basestring): k = '"%s"' % k
                if isinstance(v, basestring): v = '"%s"' % v
                # 如果是字典则递归
                if isinstance(v, dict):
                    v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
                if isinstance(v, list):
                    v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
                # case,根据(k,v)对在哪个位置确定拼接什么
                if i == 0:  # 开头,拼左花括号
                    if len(obj) == 1:
                        yield '{%s: %s}' % (k, v)
                    else:
                        yield '{%s: %s,\n' % (k, v)
                elif i == len(obj) - 1:  # 结尾,拼右花括号
                    yield '%s%s: %s}' % (indent, k, v)
                else:
                    yield '%s%s: %s,\n' % (indent, k, v)
        elif isinstance(obj, (list)):
            for i, list_node in enumerate(obj):
                if isinstance(list_node, basestring):
                    list_node = '"%s"' % list_node
                else:
                    if isinstance(list_node, dict):
                        # list_node = ''.join(_pretty(list_node, indent + ' ' * len(str(list_node) + ': {')))  # 计算下一层的indent
                        list_node = ''.join(
                            _pretty(list_node, indent + ' ' * len(':{')))
                    elif isinstance(list_node, list):
                        # list_node = ''.join(_pretty(list_node, indent + ' ' * len(str(list_node) + ': {')))  # 计算下一层的indent
                        list_node = ''.join(
                            _pretty(list_node, indent + ' ' * len(list_node)))  # 计算下一层的indent

                if i == 0:  # 开头,拼左花括号
                    if len(obj) == 1:   #如果只有一个元素
                        yield '[%s]' % list_node
                    else:   #如果超过了一个元素
                        yield '[%s,\n' % list_node
                elif i == len(obj) - 1:  # 结尾,拼右花括号
                    yield '%s%s]' % (indent, list_node)
                else:  # 中间
                    yield '%s%s,\n' % (indent, list_node)
    return ''.join(_pretty(obj, indent))

def unicode_to_str(data):
    '''
        把list或者dict中的unicode字段转换为str
        :param data:
        :return:
        '''
    if isinstance(data, (dict)):
        d = {}
        # 中文(unicode)转换成str
        for dk, dv in data.items():
            if isinstance(dk, (unicode)):
                dk = dk.encode('utf-8')
            if isinstance(dv, (unicode)):
                dv = dv.encode('utf-8')
            d[dk] = dv
    elif isinstance(data, (list)):
        d = []
        for list_v in data:
            if isinstance(list_v, (unicode)):
                list_v = list_v.encode('utf-8')
            d.append(list_v)
    return d

def get_nowtime_stamp(is_unix = False):
    '''
    获取当前时间戳
    :param is_unix: 是否unix时间戳(*1000)
    :return:
    '''
    unix_ts = time.time()
    if is_unix:
        unix_ts = long(unix_ts * 1000)
    else:
        unix_ts = long(unix_ts)
    return unix_ts
def time_stamp2time(timestamp):
    # 转换成localtime
    time_local = time.localtime(float(timestamp[:10]))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

def get_time_stamp(times, is_unix = False, times_format="%Y-%m-%d %H:%M:%S"):
    '''
    获取当前时间戳
    :param is_unix: 是否unix时间戳(*1000)
    :return:
    '''
    strTime = datetime.datetime.strptime(times, times_format)
    unix_ts = time.mktime(strTime.timetuple())
    if is_unix:
        unix_ts = long(unix_ts * 1000)
    else:
        unix_ts = long(unix_ts)
    return unix_ts

def push_pickle(data, file_name):
    path = os.path.join(os.getcwd(), 'static', 'model', 'pickle_file')
    fp = os.path.join(path, str(file_name)+'.txt')
    f = open(fp, 'wb')
    pickle.dump(data, f)
    f.close()

def pull_pickle(file_name):
    try:
        path = os.path.join(os.getcwd(), 'static', 'model', 'pickle_file')
        fp = os.path.join(path, str(file_name) + '.txt')
        with open(fp, 'rb') as f:
            data = pickle.load(f)
            return data
    except:
        return None

if __name__ == '__main__':
    s = "1514476800000"
    print time_stamp2time(s)
