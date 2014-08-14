import datetime

from drape.response import json_response
from drape.validate import validate
from drape.model import LinkedModel, F
from drape.util import toInt

from app.model import caches
from . import frame


_VALIDATES = {
    'text': {
        'name': '内容',
        'validates': [
            ('notempty', ),
            ('len', 1, 200)
        ]
    },
}


@frame.ajax_check_login
@frame.pager_ajax
def index(request, page, per_page, uid):
    params = request.params()

    to_uid = toInt(params.get('userinfo_id'), -1)
    if to_uid < 0 or to_uid == uid:
        where_data = {
            '__or': (
                {
                    'from_uid': uid,
                },
                {
                    'to_uid': uid,
                }
            )
        }
    else:
        where_data = {
            '__or': (
                {
                    'from_uid': uid,
                    'to_uid': to_uid,
                },
                {
                    'from_uid': to_uid,
                    'to_uid': uid,
                }
            )
        }

    usermsg_model = LinkedModel('usermsg')
    return usermsg_model.join(
        'userinfo',
        {
            'from_ui.id': F('usermsg.from_uid'),
        },
        'from_ui'
    ).join(
        'userinfo',
        {
            'to_ui.id': F('usermsg.to_uid')
        },
        'to_ui'
    ).where(where_data).limit(
        per_page
    ).offset(
        per_page * page
    ).order(
        'usermsg.ctime', 'DESC'
    ).select_and_count()


@frame.ajax_check_login
def create(request, uid):
    params = request.params()

    # validates
    validate(params, _VALIDATES)

    # params
    to_uid = toInt(params.get('userinfo_id'), -1)
    text = params.get('text')
    now = datetime.datetime.now()

    # insert to db
    usermsg_model = LinkedModel('usermsg')
    usermsg_id = usermsg_model.insert(
        from_uid=uid,
        to_uid=to_uid,
        text=text,
        ctime=now
    )

    # notice
    notice_model = LinkedModel('notice')
    notice_model.insert(
        from_uid=uid,
        to_uid=to_uid,
        item_id=usermsg_id,
        type='usermsg',
        ctime=now,
        isRead=False
    )
    caches.get_notice_count.remove(to_uid)

    return json_response({
        'result': 'success',
        'msg': '留言成功'
    })
