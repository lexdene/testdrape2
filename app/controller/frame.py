# -*- coding: utf-8 -*-
'some common functions that all controllers need'

import re
import inspect
from functools import wraps

import drape
from drape.util import tile_list_data, toInt
from drape.response import json_response
from drape import http

import app
from app.model import caches


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
        'create a new resource level'
        res = Resource(path)
        self.__levels.append(res)
        return res

    def add(self, path=None, res_type=('js', 'css'), version=0):
        'add resource'
        if path is None:
            path = self.__path

        if isinstance(res_type, tuple):
            for i in res_type:
                self.add(path, i, version)
        else:
            self.__resources.append(dict(
                path=path,
                res_type=res_type,
                version=version
            ))


def html_body(request, variables, path=None):
    'frame by html body'
    if path is None:
        path = request.path()[1:]

    variables['ROOT'] = request.root_path()

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
            'title': variables.get('title', '无标题'),
            'my_userid': uid,
            # pylint: disable=no-member
            'coffee_debug': drape.config.COFFEE_IS_DEBUG,
            'version': app.version,
            'drape_version': drape.version,
            'body': body,
            'LIBCDN': drape.config.LIBCDN,  # pylint: disable=no-member
        }
    )

    return drape.response.Response(
        body=html
    )


def default_frame(request, variables, path=None):
    'frame by default frame'
    # path
    if path is None:
        cur_frame = inspect.currentframe()
        back_frame = cur_frame.f_back
        back_module = inspect.getmodule(back_frame)

        match = re.match(
            r'^app\.controller\.(.*)$',
            back_module.__name__
        )
        if match is None:
            raise ValueError(
                'module name error: %s' % (
                    back_module.__name__
                )
            )

        path = '%s/%s' % (
            match.group(1).replace('.', '/'),
            back_frame.f_code.co_name
        )

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

    content = drape.render.render(
        path,
        variables
    )

    if uid > 0:
        userinfo = caches.get_userinfo(uid)
        notice_count = caches.get_notice_count(uid)
        mail_count = caches.get_mail_count(uid)
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
            'title': variables.get('title', '无标题'),
        },
        'frame/Layout'
    )


def show_error_page(request, message):
    'show error page'
    return default_frame(
        request,
        {
            'title': '错误',
            'error': message
        },
        'frame/Error'
    )


def pager_ajax(func):
    ''' 为ajax请求封装pager相关操作 '''
    @wraps(func)
    def pager_controller(request, *argv, **kwargs):
        ''' 处理分页请求 '''
        # page
        params = request.params()
        page = toInt(params.get('page', 0))
        per_page = toInt(params.get('per_page', 20))

        if per_page > 100:
            per_page = 100

        data, count = func(request, page, per_page, *argv, **kwargs)

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
            raise http.Unauthorized()

        return fun(request, uid)

    return new_fun
