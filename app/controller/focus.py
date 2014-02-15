# -*- coding: utf-8 -*-
'''
    关注模块
'''

import datetime

from drape.controller import JsonController
from drape.util import toInt
from drape.model import LinkedModel

from app.lib.cache import remove_cache


class ajaxFocus(JsonController):
    '''
        focus or unfocus user / topic / tag by ajax
    '''
    def process(self):
        # current user id
        aSession = self.session()
        current_uid = toInt(aSession.get('uid', -1))
        if current_uid < 0:
            self.set_variable('result', 'failed')
            self.set_variable('msg', u'请先登录')
            return

        # target type and target id
        aParams = self.params()
        focus_type = aParams.get('type', '')
        target_id = toInt(aParams.get('target', -1))
        dire = aParams.get('dire', '')

        # check param
        if not focus_type in ('user', 'topic', 'tag'):
            self.set_variable('result', 'failed')
            self.set_variable('msg', u'参数非法: type')
            return

        if target_id < 0:
            self.set_variable('result', 'failed')
            self.set_variable('msg', u'参数非法: target')
            return

        if not dire in ('add', 'remove'):
            self.set_variable('result', 'failed')
            self.set_variable('msg', u'参数非法: dire')
            return

        if current_uid == target_id and 'user' == focus_type:
            self.set_variable('result', 'failed')
            self.set_variable('msg', u'不可以关注自己')
            return

        # check repeat
        aFocusModel = LinkedModel('focus')
        if 'add' == dire and aFocusModel.where(
            from_uid=current_uid,
            focus_type=focus_type,
            target_id=target_id,
            is_del=False
        ).find():
            self.set_variable('result', 'failed')
            self.set_variable('msg', u'已经关注，不可以重复关注')
            return

        # save to db
        now = datetime.datetime.now()
        if 'add' == dire:
            focus_id = aFocusModel.insert(
                from_uid=current_uid,
                focus_type=focus_type,
                target_id=target_id,
                ctime=now,
                is_del=False
            )

            # add action
            aActionModel = LinkedModel('action')
            aActionModel.insert(
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
            aFocusModel.where(
                from_uid=current_uid,
                focus_type=focus_type,
                target_id=target_id
            ).update(
                is_del=True
            )

        self.set_variable('result', 'success')
        self.set_variable('msg', '')


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
