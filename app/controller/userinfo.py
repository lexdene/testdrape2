# -*- coding: utf-8 -*-

from drape.util import toInt
from drape.model import LinkedModel
from drape.response import json_response

from app.lib.text import datetime2Str, avatarFunc
from . import frame
from .focus import isFocused

def ajax_user_info(request):
    ''' ajax获取用户资料 '''
    # uid
    params = request.params()
    uid = toInt(params.get('uid'), 0)

    # user info
    userinfo_model = LinkedModel('userinfo')
    userinfo = userinfo_model.where(id=uid).find()
    if userinfo is None:
        return json_response({
            'uid': uid,
            'result': 'failed',
            'msg': u'无此用户'
        })

    # topic count
    userinfo['topic_count'] = LinkedModel(
        'discuss_topic'
    ).where(
        uid=uid
    ).count()

    # reply count
    userinfo['reply_count'] = LinkedModel(
        'discuss_reply'
    ).where(
        uid=uid
    ).count()

    # response
    return json_response({
        'uid': uid,
        'result': 'success',
        'userinfo': userinfo
    })


def MainPage(request):
    params = request.params()
    uid = toInt(params.get('id', 0))

    userinfo_model = LinkedModel('userinfo')
    userinfo = userinfo_model.where(id=uid).find()
    if userinfo is None:
        return frame.Error(request, u'无此用户')

    return frame.default_frame(
        request,
        {
            'title': userinfo['nickname'],
            'userinfo': userinfo,
            'timestr': datetime2Str,
            'avatar': avatarFunc(request),
            'isFocused': isFocused(request, 'user', uid)
        }
    )
