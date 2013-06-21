# -*- coding: utf-8 -*-

import time

from drape.controller import jsonController
from drape.util import toInt
from drape.model import LinkedModel

class ajaxFocus(jsonController):
    def process(self):
        # current user id
        aSession = self.session()
        current_uid = toInt(aSession.get('uid', -1))
        if current_uid < 0:
            self.setVariable('result', 'failed')
            self.setVariable('msg', u'请先登录')
            return

        # target type and target id
        aParams = self.params()
        focus_type = aParams.get('type', '')
        target_id = toInt(aParams.get('target', -1))
        dire = aParams.get('dire', '')

        # check param
        if not focus_type in ('user', 'topic', 'tag'):
            self.setVariable('result', 'failed')
            self.setVariable('msg', u'参数非法: type')
            return

        if target_id < 0:
            self.setVariable('result', 'failed')
            self.setVariable('msg', u'参数非法: target')
            return

        if not dire in ('add', 'remove'):
            self.setVariable('result', 'failed')
            self.setVariable('msg', u'参数非法: dire')
            return

        if current_uid == target_id and 'user' == focus_type:
            self.setVariable('result', 'failed')
            self.setVariable('msg', u'不可以关注自己')
            return

        # check repeat
        aFocusModel = LinkedModel('focus')
        if 'add' == dire and aFocusModel.where(
            from_uid=current_uid,
            focus_type=focus_type,
            target_id=target_id,
            is_del=False
        ).find():
            self.setVariable('result', 'failed')
            self.setVariable('msg', u'已经关注，不可以重复关注')
            return

        # save to db
        now = int(time.time())
        if 'add' == dire:
            aFocusModel.insert(
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
        elif 'remove' == dire:
            aFocusModel.where(
                from_uid=current_uid,
                focus_type=focus_type,
                target_id=target_id
            ).update(
                is_del=True
            )

        self.setVariable('result', 'success')
        self.setVariable('msg', '')


def isFocused(controller, focus_type, target_id):
    # current user id
    aSession = controller.session()
    current_uid = toInt(aSession.get('uid', -1))

    aFocusModel = LinkedModel('focus')
    if aFocusModel.where(
        from_uid=current_uid,
        focus_type=focus_type,
        target_id=target_id,
        is_del=False
    ).find():
        return True

    return False
