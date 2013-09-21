# -*- coding: utf-8 -*-
''' 简单封装一下 memcache '''

import memcache

from drape import config


class Cache(object):
    ''' 简单封装一下 memcache '''
    def __init__(self):
        self.__connection = memcache.Client([
            '%s:%s' % (
                config.CACHE_HOST,
                config.CACHE_PORT
            )
        ])

    def get(self, key, func):
        '''
            获取某值
            如果缓存中没有
            则从func中获取值
            然后保存到缓存中
        '''
        value = self.__connection.get(key)
        if value is None:
            value = func()
            self.__connection.set(
                key,
                value,
                time=config.CACHE_EXPIRE_TIME
            )
        return value

    def remove(self, key):
        ''' 从缓存中删除一个值 '''
        self.__connection.delete(key)


def remove_cache(key):
    cache = Cache()
    cache.remove(key)
