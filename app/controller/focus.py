# -*- coding: utf-8 -*-
'''
    关注模块
'''

import datetime

from drape.util import toInt
from drape.model import LinkedModel
from drape.response import json_response

from app.lib.cache import remove_cache


def ajax_focus(request):
    '''
        focus or unfocus user / topic / tag by ajax
    '''
    # current user id
    session = request.session
    current_uid = toInt(session.get('uid', -1))
    if current_uid < 0:
        return json_response({
            'result': 'failed',
            'msg': u'请先登录'
        })

    # target type and target id
    params = request.params()
    focus_type = params.get('type', '')
    target_id = toInt(params.get('target', -1))
    dire = params.get('dire', '')

    # check param
    if not focus_type in ('user', 'topic', 'tag'):
        return json_response({
            'result': 'failed',
            'msg': u'参数非法: type'
        })

    if target_id < 0:
        return json_response({
            'result': 'failed',
            'msg': u'参数非法: target'
        })

    if not dire in ('add', 'remove'):
        return json_response({
            'result': 'failed',
            'msg': u'参数非法: dire'
        })

    if current_uid == target_id and 'user' == focus_type:
        return json_response({
            'result': 'failed',
            'msg': u'不可以关注自己'
        })

    # check repeat
    focus_model = LinkedModel('focus')
    if 'add' == dire and focus_model.where(
        from_uid=current_uid,
        focus_type=focus_type,
        target_id=target_id,
        is_del=False
    ).find():
        return json_response({
            'result': 'failed',
            'msg': u'已经关注，不可以重复关注'
        })

    # save to db
    now = datetime.datetime.now()
    if 'add' == dire:
        # same but deleted focus
        exist_deleted_focus = focus_model.where(
            from_uid=current_uid,
            focus_type=focus_type,
            target_id=target_id,
            is_del=True
        ).find()

        if exist_deleted_focus:
            focus_id = exist_deleted_focus['id']
            focus_model.where(
                id=focus_id
            ).update(
                ctime=now,
                is_del=False
            )
        else:
            focus_id = focus_model.insert(
                from_uid=current_uid,
                focus_type=focus_type,
                target_id=target_id,
                ctime=now,
                is_del=False
            )

        # add action
        LinkedModel('action').insert(
            from_object_id=current_uid,
            from_object_type='user',
            action_type='focus',
            target_object_id=target_id,
            target_object_type=focus_type,
            ctime=now
        )

        # add notice
        if 'user' == focus_type:
            notice_model = LinkedModel('notice')
            notice_model.insert(
                from_uid=current_uid,
                to_uid=target_id,
                item_id=focus_id,
                type='focus_user',
                ctime=now,
                isRead=False
            )
            remove_cache('notice_count/%s' % target_id)

    elif 'remove' == dire:
        focus_model.where(
            from_uid=current_uid,
            focus_type=focus_type,
            target_id=target_id
        ).update(
            is_del=True
        )

    return json_response({
        'result': 'success',
        'msg': ''
    })


def isFocused(request, focus_type, target_id):
    # current user id
    session = request.session
    current_uid = toInt(session.get('uid', -1))

    # find in db
    if LinkedModel('focus').where(
        from_uid=current_uid,
        focus_type=focus_type,
        target_id=target_id,
        is_del=False
    ).find():
        return True

    return False
