# -*- coding: utf-8 -*-
''' 简单封装一下 memcache '''

from functools import wraps
import memcache

from drape import config


class Cache(object):
    ''' 简单封装一下 memcache '''
    def __init__(self):
        self.__connection = memcache.Client([
            '%s:%s' % (
                # pylint: disable=no-member
                config.CACHE_HOST, config.CACHE_PORT
            )
        ])

    def set(self, key, value):
        'save value in cache'
        self.__connection.set(key, value)

    def get(self, key, default_value=None):
        'get value from cache'
        value = self.__connection.get(key)
        if value is None:
            return default_value
        else:
            return value

    def remove(self, key):
        ''' 从缓存中删除一个值 '''
        self.__connection.delete(key)


def cache_by(key_tmpl):
    '''
        a cache_by decorator
        auto call function if value not in cache
    '''
    cache = Cache()

    def cache_deco(func):
        'function decorator'

        @wraps(func)
        def cache_value_generator(*argv):
            'real function'
            key = key_tmpl % argv
            value = cache.get(key)
            if value is None:
                value = func(*argv)
                cache.set(key, value)

            return value

        return cache_value_generator

    return cache_deco
