# -*- coding: utf-8 -*-

import datetime

from drape.util import md5sum, random_str, pick_dict
from drape.response import json_response
from drape.http import post_only
from drape.validate import validate_params
from drape.model import LinkedModel
from drape import config

from . import frame
from app.lib import validate_code

_common_validates = {
    'loginname': {
        'name': '登录名',
        'validates': (
            ('notempty',),
            ('len', 4, 20),
        )
    },
    'password': {
        'name': '密码',
        'validates': (
            ('notempty',),
            ('len', 4, 20)
        )
    },
    'repassword': {
        'name': '重复密码',
        'validates': (
            ('notempty',),
            ('equal', 'password')
        ),
    },
    'nickname': {
        'name': '昵称',
        'validates': (
            ('notempty',),
            ('len', 4, 20)
        )
    },
    'email': {
        'name': '昵称',
        'validates': (
            ('notempty',),
            ('email',)
        )
    },
    'intro': {
        'name': '个人介绍',
        'validates': (
            ('notempty',),
            ('len', 4, 1000)
        )
    }
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


def password_for_db(password):
    ''' 将加密后的密码保存到数据库时，还要保存salt '''
    salt = random_str(8)
    return '%s#%s' % (
        salt,
        encrypt_password(
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
            'title': '登录',
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
            'msg': '验证码错误'
        })

    # validate params
    result = validate_params(
        params,
        pick_dict(
            _common_validates,
            ('loginname', 'password')
        )
    )
    if result:
        return json_response({
            'result': 'failed',
            'msg': '填写内容不符合要求',
            'validate_result': result,
        })

    # login model
    login_model = LinkedModel('logininfo')
    login_info = login_model.where(
        loginname=params['loginname']
    ).find()
    if login_info is None:
        return json_response({
            'result': 'failed',
            'msg': '登录名不存在'
        })
    elif not validate_password(
        params['password'],
        login_info['password']
    ):
        return json_response({
            'result': 'failed',
            'msg': '密码错误'
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


def Logout(request):
    session = request.session
    session.remove('uid')

    params = request.params()
    return frame.default_frame(
        request,
        {
            'title': '退出登录',
            'redirect': params.get('redirect', ''),
        }
    )


def Register(request):
    return frame.default_frame(
        request,
        {
            'title': '注册',
            'redirect': request.params().get('redirect', '/'),
        }
    )


@post_only
def ajaxRegister(request):
    params = request.params()

    # validate code
    if not validate_code.validate(
        request,
        params.get('valcode', '')
    ):
        return json_response({
            'result': 'failed',
            'msg': '验证码错误'
        })

    # validate params
    result = validate_params(
        params,
        pick_dict(
            _common_validates,
            (
                'loginname', 'password', 'repassword',
                'nickname', 'email', 'intro'
            )
        )
    )
    if result:
        return json_response({
            'result': 'failed',
            'msg': '填写内容不符合要求',
            'validate_result': result,
        })

    # db model
    login_model = LinkedModel('logininfo')

    # already exist same loginname
    exist_user = login_model.where(
        loginname=params.get('loginname')
    ).exist()
    if exist_user:
        return json_response({
            'result': 'failed',
            'msg': '存在登录名相同的用户'
        })

    # save to db
    user_id = login_model.insert(
        loginname=params.get('loginname'),
        password=password_for_db(
            params.get('password')
        )
    )

    # user info
    user_model = LinkedModel('userinfo')
    user_model.insert(
        id=user_id,
        nickname=params.get('nickname'),
        email=params.get('email'),
        intro=params.get('intro'),
        ctime=datetime.datetime.now(),
        score=0
    )

    # response
    return json_response({
        'result': 'success',
        'id': user_id
    })
