#coding=utf-8

def add(a,b):
    c =a +b
    return c

class JiSuan(object):
    @classmethod
    def add(cls, a,b):
        return a+b
    def sub(self, a,b):
        return a-b
    def data(self):
        return '<a href="http://www.baidu.com">百度</a>'
    def args(self,*args):
        return [a+"----aaa" for a in args[0]]
