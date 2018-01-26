# -*- coding: utf8 -*-
__author__ = 'Alex.xu'
# di = {"name":"test1", "sex":"test2", "others":[1,2,"3"]}
# print di

# def pretty_dict(obj, indent=' '):
#     def _pretty(obj, indent):
#         for i, tup in enumerate(obj.items()):
#             k, v = tup
#             #如果是字符串则拼上""
#             if isinstance(k, basestring): k = '"%s"'% k
#             if isinstance(v, basestring): v = '"%s"'% v
#             #如果是字典则递归
#             if isinstance(v, dict):
#             v = ''.join(_pretty(v, indent + ' '* len(str(k) + ': {')))#计算下一层的indent
#             #case,根据(k,v)对在哪个位置确定拼接什么
#             if i == 0:#开头,拼左花括号
#             if len(obj) == 1:
#              yield '{%s: %s}'% (k, v)
#             else:
#              yield '{%s: %s,\n'% (k, v)
#             elif i == len(obj) - 1:#结尾,拼右花括号
#             yield '%s%s: %s}'% (indent, k, v)
#             else:#中间
#             yield '%s%s: %s,\n'% (indent, k, v)
#             print ''.join(_pretty(obj, indent))
#

# coding=utf-8
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
                else:  # 中间
                    yield '%s%s: %s,\n' % (indent, k, v)
        elif isinstance(obj, (list)):
            for i, list_node in enumerate(obj):
                if isinstance(list_node, basestring):
                    list_node = '"%s"' % list_node
                else:
                    if isinstance(list_node, dict):
                        # list_node = ''.join(_pretty(list_node, indent + ' ' * len(str(list_node) + ': {')))  # 计算下一层的indent
                        list_node = ''.join(
                            _pretty(list_node, indent + ' ' * len(':{')))  # 计算下一层的indent
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

d = {"root": {"folder2": {"item2": None, "item1": None},
              "folder1": {"subfolder1": {"item2": "你好啊", "item1": [122222,2,"你好啊"]}, "subfolder2": {"item3": None}}}}
d2 = ['a','b','c',{'d':[1,2,3]}]
d3 = {'d':[1,2,3], 'b':[{'a':[1,222222222222,'好好']}, 1,2,3]}
print pretty_dict2(d3)
# import json
# di = {"name":"test1", "sex":"test2", "others":['你好',2,"3"]}
# print json.dumps(di, indent=4)
