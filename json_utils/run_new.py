# -*- coding: utf8 -*-
__author__ = 'Alex.xu'

import sys
class Stack():
    def __init__(self):
        self.stack = []
        self.top = -1
    def push(self, x):
        self.stack.append(x)
        self.top = self.top + 1
    def pop(self):
        ''''''
        if self.is_empty():
            raise exception("stack is empty")
        else:
            self.top = self.top - 1
            self.stack.pop()
    def is_empty(self):
        return self.top == -1
    def peek(self):
        '''
        :return:栈顶元素
        '''
        if self.stack is not []:
            return self.stack[self.top]
        else:
            return None

class Bracket():
    @classmethod
    def is_right_bracket(self, ch):
        '''
        判断是否为右括号
        :return: boolean
        '''
        # if ch == ')' or ch == ']' or ch == '}':
        if ch == '}':
            return True;
        else:
            return False;

    @classmethod
    def is_left_bracket(self, ch):
        '''
        判断是否为左括号
        :return: boolean
        '''
        # if ch == '(' or ch == '[' or ch == '{':
        if ch == '{':
            return True;
        else:
            return False;
    @classmethod
    def is_peek(self, peek, c):
        # brackets = ['{', '[', '(', ')', ']', '}']
        brackets = ['{', '}']
        temp = 0
        for i in brackets[len(brackets)/2:]:
            if c == i:
                if peek == brackets[temp]:
                    return True
            temp += 1
        return False

def substr(str, start, end):
    return str[str.index(start) + len(start):str.index(end, str.index(start))]

def getPeek(str, flag=None):
    '''
    返回字符串指定括号匹配内容
    :param flag:
    :return:
    '''
    s = Stack()
    temp = False
    start = 0
    for index, c in enumerate(str):
        if Bracket.is_left_bracket(c):
            if temp is False:
                start = index
            temp = True
            s.push(c)
        elif Bracket.is_right_bracket(c):
            if s.is_empty():
                raise exception("peek fail!")
            elif Bracket.is_peek(s.peek(), c) is not None:
                s.pop()
        if temp is True:#
            if s.is_empty():
                return str[start:index+1]

def my_split(flag, s):
    '''
    分割字符串,不分割${}里面的
    :param flag: 根据什么字符分割
    :param s: 要分割的字符串
    :return:
    '''
    data = s.split(flag)
    a = []
    stack = Stack()
    temp = ''
    for d in data:
        if stack.is_empty():
            temp += d
        else:
            temp = temp+','+d
        if '${' in d or not stack.is_empty():
            # temp = ',' + d
            for c in d:
                if Bracket.is_left_bracket(c):
                    stack.push(c)
                elif Bracket.is_right_bracket(c):
                    if stack.is_empty():
                        raise exception("peek fail!")
                    elif Bracket.is_peek(stack.peek(), c) is not None:
                        stack.pop()
            if stack.is_empty():
                a.append(temp)
                temp = ''
        else:
            a.append(d)
            temp = ''
    return a

if __name__ == "__main__":
    s = '${ab,c[]},b,c,d,${a,b,c,d}abc,${[a,b,c,d]},'

    for i in my_split(',', s):
        print i