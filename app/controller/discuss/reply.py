import datetime

from drape.model import LinkedModel, F
from drape.util import toInt, pick_dict
from drape.response import json_response
from drape.validate import validate_params

from app.model import caches
from .. import frame


_common_validates = {
    'title': {
        'name': '标题',
        'validates': (
            ('notempty',),
            ('len', 4, 50)
        )
    },
    'text': {
        'name': '内容',
        'validates': (
            ('notempty',),
            ('len', 4, 500)
        )
    },
    'tid': {
        'name': '主题id',
        'validates': (
            ('int',),
        )
    },
    'reply_to_id': {
        'name': '回复id',
        'validates': (
            ('int',),
        )
    },
}


def index(request):
    raise ValueError(request.params())


@frame.ajax_check_login
def create(request, uid):
    params = request.params()

    # validates
    result = validate_params(
        params,
        pick_dict(
            _common_validates,
            ('tid', 'reply_to_id', 'text')
        )
    )
    if result:
        return json_response({
            'result': 'failed',
            'msg': '填写内容不符合要求',
            'validate_result': result,
        })

    # params
    tid = toInt(params['tid'])
    reply_to_id = toInt(params['reply_to_id'])
    text = params['text']
    now = datetime.datetime.now()

    # reply model
    reply_model = LinkedModel('discuss_reply')
    reply_id = reply_model.insert(
        tid=tid,
        uid=uid,
        reply_to_id=reply_to_id,
        ctime=now,
        text=text
    )

    # topic cached model
    topic_cache_model = LinkedModel('discuss_topic_cache')
    topic_cache_model.where(
        id=tid
    ).update(
        last_reply_id=reply_id
    )

    # topic info
    topic_info = LinkedModel('discuss_topic').where(
        id=tid
    ).find()

    # reply to reply info
    reply_to_reply_info = reply_model.where(
        id=reply_to_id
    ).find()

    # notice model
    notice_model = LinkedModel('notice')
    notice_cache_model = LinkedModel('notice_cache')

    # reply topic notice
    # except to myself
    if topic_info['uid'] != uid and (
        not reply_to_reply_info
        or
        reply_to_reply_info['uid'] != topic_info['uid']
    ):
        notice_model.insert(
            from_uid=uid,
            to_uid=topic_info['uid'],
            item_id=reply_id,
            type='reply_topic',
            ctime=now,
            isRead=False
        )
        caches.get_notice_count.remove(uid)

    # reply to reply notice
    # except to myself
    if reply_to_reply_info and uid != reply_to_reply_info['uid']:
        notice_model.insert(
            from_uid=uid,
            to_uid=reply_to_reply_info['uid'],
            item_id=reply_id,
            type='reply_to_reply',
            ctime=now,
            isRead=False
        )
        caches.get_notice_count.remove(topic_info['uid'])

    # action
    # user reply topic
    action_model = LinkedModel('action')
    action_model.insert(
        from_object_id=uid,
        from_object_type='user',
        action_type='reply',
        target_object_id=reply_id,
        target_object_type='reply',
        ctime=now
    )

    # topic has reply
    action_model.insert(
        from_object_id=tid,
        from_object_type='topic',
        action_type='reply',
        target_object_id=reply_id,
        target_object_type='reply',
        ctime=now
    )

    # remove cache
    caches.get_topic_info.remove(tid)

    # success
    return json_response({
        'result': 'success',
        'msg': '回复成功'
    })

