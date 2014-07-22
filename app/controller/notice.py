# -*- coding: utf-8 -*-
''' 跟通知有关的模块 '''
from drape.model import LinkedModel, F
from drape.util import tile_list_data
from drape.response import json_response

from . import frame

@frame.ajax_check_login
def index(request, uid):
    ''' 未读消息列表 '''
    notice_model = LinkedModel('notice')
    notice_list = notice_model.join(
        'userinfo',
        {
            'fromuser.id': F('notice.from_uid')
        },
        'fromuser'
    ).where(
        to_uid=uid,
        isRead=0
    ).limit(
        10
    ).select()

    reply_model = LinkedModel('discuss_reply')

    # notice list
    for notice in notice_list:
        if notice['type'] in ('reply_topic', 'reply_to_reply'):
            notice['reply_info'] = reply_model.alias(
                're'
            ).join(
                'discuss_topic',
                {
                    'dt.id': F('re.tid')
                },
                'dt'
            ).where({
                're.id': notice['item_id']
            }).find()
        elif notice['type'] in ('focus_user', 'usermsg'):
            pass
        else:
            raise ValueError('no such type: %s' % notice['type'])

    return json_response(tile_list_data(notice_list))


@frame.ajax_check_login
def ajax_set_is_read(self):
    ''' 将消息设置成已读 '''
    session = self.session()
    uid = toInt(session.get('uid', -1))

    params = self.params()
    notice_id = toInt(params.get('notice_id', -1))
    self.set_variable('notice_id', notice_id)

    notice_model = LinkedModel('notice')
    notice_info = notice_model.where(id=notice_id).find()
    self.set_variable('notice_info', notice_info)

    if notice_info is None:
        self.set_variable('result', 'failed')
        self.set_variable('msg', 'no such notice')
        return

    if notice_info['to_uid'] != uid:
        self.set_variable('result', 'failed')
        self.set_variable('msg', 'notice is not for you')
        return

    notice_model.where(id=notice_id).update(isRead=1)

    self.set_variable('result', 'success')

    remove_cache('notice_count/%s' % uid)
