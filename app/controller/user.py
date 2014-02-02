# -*- coding: utf-8 -*-

from drape.util import md5sum, random_str
from drape import config

from . import frame

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
