# -*- coding: utf-8 -*-
'''
    与登录相关的公用方法
    版本: 1.0
'''

from functools import wraps

from drape.util import toInt


def check_login(fun):
    '''
    装饰器
    在显示页面中判断是否登录
    未登录，则显示NotLogin
    '''
    @wraps(fun)
    def new_fun(self):
        '''
        check login
        先执行fun为了让它设置title等属性
        '''
        fun(self)

        session = self.session()
        uid = toInt(session.get('uid', -1))
        if uid < 0:
            self.notLogin()

    return new_fun
