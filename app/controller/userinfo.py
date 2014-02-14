# -*- coding: utf-8 -*-

from drape.util import toInt
from drape.model import LinkedModel
from drape.response import json_response


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
