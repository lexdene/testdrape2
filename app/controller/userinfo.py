# -*- coding: utf-8 -*-

from drape.util import toInt
from drape.model import LinkedModel
from drape.response import json_response
import drape.http

from app.lib.text import datetime2Str, avatarFunc
from . import frame
from .focus import isFocused


def show(request):
    ''' ajax获取用户资料 '''
    # uid
    params = request.params()
    uid = toInt(params.get('userinfo_id'), 0)

    # user info
    userinfo_model = LinkedModel('userinfo')
    userinfo = userinfo_model.where(id=uid).find()
    if userinfo is None:
        raise drape.http.NotFound('record not found')

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

    # response by accept
    accept = request.chief_accept()
    if accept == 'application/json':
        return json_response(userinfo)
    else:
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
