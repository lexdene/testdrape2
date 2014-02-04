# -*- coding: utf-8 -*-

from drape.util import md5sum, random_str, pick_dict
from drape.response import json_response
from drape.http import post_only
from drape.validate import validate_params
from drape.model import LinkedModel
from drape import config

from . import frame
from app.lib import validate_code

_common_validates = {
    'password': {
        'key': 'password',
        'name': u'密码',
        'validates': (
            ('notempty',),
            ('len', 4, 20)
        )
    },
    'repassword': {
        'key': 'repassword',
        'name': u'重复密码',
        'validates': (
            ('notempty',),
            ('equal', 'password')
        ),
    },
    'loginname': {
        'key': 'loginname',
        'name': u'登录名',
        'validates': (
            ('notempty',),
            ('len', 4, 20),
        )
    },
}


def encrypt_password(password, salt=None):
    if salt is None:
        salt = random_str(8)

    return md5sum(
        '%s|%s' % (
            password,
            salt
        )
    )


def validate_password(source, encrypted):
    salt, hashed = encrypted.split('#')
    return hashed == encrypt_password(source, salt)


def Login(request):
    params = request.params()

    return frame.default_frame(
        request,
        {
            'title': u'登录',
            'redirect': params.get('redirect', '/home'),
            'autologin_daylength': config.AUTOLOGIN_DAY_LENGTH
        }
    )


@post_only
def ajaxLogin(request):
    params = request.params()

    # validate code
    if not validate_code.validate(
        request,
        params.get('valcode', '')
    ):
        return json_response({
            'result': 'failed',
            'msg': u'验证码错误'
        })

    # validate params
    result = validate_params(
        params,
        pick_dict(
            _common_validates,
            ('loginname', 'password')
        ).values()
    )
    if not result['result']:
        return json_response({
            'result': 'failed',
            'msg': result['msg']
        })

    # login model
    login_model = LinkedModel('logininfo')
    login_info = login_model.where(
        loginname=params['loginname']
    ).find()
    if login_info is None:
        return json_response({
            'result': 'failed',
            'msg': u'登录名不存在'
        })
    elif not validate_password(
        params['password'],
        login_info['password']
    ):
        return json_response({
            'result': 'failed',
            'msg': u'密码错误'
        })
    else:
        session = request.session
        session.set('uid', login_info['id'])

        # 自动登录
        if params.get('autologin', 'off') == 'on':
            expired = int(
                params['autologin_daylength']
            ) * 24 * 3600
            session.set_cookie_attr(expired=expired)

        return json_response({
            'result': 'success'
        })
