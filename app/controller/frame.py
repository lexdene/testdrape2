# -*- coding: utf-8 -*-

from functools import wraps

import drape
from drape.util import tile_list_data, toInt
from drape.model import LinkedModel
from drape.response import json_response

import app
from app.lib.cache import Cache


class Resource(object):
    '''
    管理css / js等资源
    '''
    def __init__(self, path=None):
        self.__levels = list()
        self.__resources = list()
        self.__path = path

    def __iter__(self):
        for level in reversed(self.__levels):
            for res in level:
                yield res

        for res in self.__resources:
            yield res

    def create_level(self, path):
        res = Resource(path)
        self.__levels.append(res)
        return res

    def add(self, path, type=('js', 'css'), version=0):
        if isinstance(type, tuple):
            for i in type:
                self.add(path, i, version)
        else:
            self.__resources.append(dict(
                path=path,
                type=type,
                version=version
            ))

    def addResByPath(self, type=('js', 'css'), version=0):
        path = self.__path
        self.add(path, type, version)


def html_body(request, variables, path=None):
    if path is None:
        path = request.controller_path

    variables['ROOT'] = request.root_path()
    variables['LIBCDN'] = drape.config.LIBCDN

    if request.res is None:
        request.res = Resource()

    variables['res'] = request.res.create_level(path)

    body = drape.render.render(
        path,
        variables
    )

    uid = request.session.get('uid', -1)
    html = drape.render.render(
        'frame/HtmlBody',
        {
            'reslist': request.res,
            'ROOT': request.root_path(),
            'title': variables.get('title', u'无标题'),
            'my_userid': uid,
            'coffee_debug': drape.config.COFFEE_IS_DEBUG,
            'version': app.version,
            'drape_version': drape.version,
            'body': body,
            'LIBCDN': drape.config.LIBCDN,
        }
    )

    return drape.response.Response(
        body=html
    )


def default_frame(request, variables, path=None):
    # path
    if path is None:
        path = request.controller_path

    # uid
    session = request.session
    uid = session.get('uid', -1)

    # res
    request.res = Resource()
    res_level = request.res.create_level(path)

    # render content
    variables['uid'] = uid
    variables['res'] = res_level
    variables['ROOT'] = request.root_path()
    variables['LIBCDN'] = drape.config.LIBCDN

    content = drape.render.render(
        path,
        variables
    )

    if uid > 0:
        cache = Cache()
        userinfo = cache.get(
            'userinfo/%s' % uid,
            lambda: LinkedModel('userinfo').where(id=uid).find()
        )

        notice_count = cache.get(
            'notice_count/%s' % uid,
            lambda: LinkedModel('notice').where(
                    to_uid=uid,
                    isRead=0,
                ).count()
        )

        mail_count = cache.get(
            'mail_count/%s' % uid,
            lambda: LinkedModel('mail').where(
                    to_uid=uid,
                    isRead=0
                ).count()
        )
    else:
        userinfo = None
        notice_count = 0
        mail_count = 0

    return html_body(
        request,
        {
            'uid': uid,
            'userinfo': userinfo,
            'notice_count': notice_count,
            'mail_count': mail_count,
            'body': content,
            'title': variables.get('title', u'无标题'),
        },
        'frame/Layout'
    )


def Error(request, message):
    return default_frame(
        request,
        {
            'title': u'错误',
            'error': message
        },
        'frame/Error'
    )


def pager_ajax(func):
    ''' 为ajax请求封装pager相关操作 '''
    @wraps(func)
    def pager_controller(request):
        ''' 处理分页请求 '''
        # page
        params = request.params()
        page = toInt(params.get('page', 0))
        per_page = toInt(params.get('per_page', 20))

        data, count = func(request, page, per_page)

        return json_response(
            tile_list_data(data),
            headers={
                'X-Record-Page': page,
                'X-Record-PerPage': per_page,
                'X-Record-Count': count
            }
        )

    return pager_controller


def ajax_check_login(fun):
    '''
        装饰器
        在ajax接口中判断是否登录
        未登录，则返回失败信息
    '''
    @wraps(fun)
    def new_fun(request):
        ''' check login before fun '''
        session = request.session
        uid = toInt(session.get('uid', -1))
        if uid < 0:
            return json_response({
                'result': 'failed',
                'msg': u'请先登录'
            })

        return fun(request, uid)

    return new_fun
