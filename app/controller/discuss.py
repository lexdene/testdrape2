# -*- coding: utf-8 -*-

import datetime

import drape
from drape.model import LinkedModel
from drape.util import toInt, pick_dict
from drape.response import json_response
from drape.http import post_only
from drape.validate import validate_params

from app.lib.text import datetime2Str, avatarFunc
from app.model.discuss import TopicModel, add_new_topic
from app.lib.tags import Tags

from . import widget, frame

DEFAULT_CONTROLLER = 'List'


_common_validates = {
    'title': {
        'name': u'标题',
        'validates': (
            ('notempty',),
            ('len', 4, 50)
        )
    },
    'text': {
        'name': u'内容',
        'validates': (
            ('notempty',),
            ('len', 4, 500)
        )
    },
}


def List(request):
    params = request.params()
    tagid = toInt(params.get('tag', 0))

    # where for topic model
    where_obj = None

    # tag info
    if tagid > 0:
        tag_model = LinkedModel('tag')
        tag_info = tag_model.where(id=tagid).find()

        tag_bridge_model = LinkedModel('discuss_topic_tag_bridge')
        tag_info['topic_count'] = tag_bridge_model.where(
            tag_id=tagid
        ).count()

        title = u'标签: %s' % tag_info['content']

        where_obj = {
            'ttb.tag_id': tagid
        }
    else:
        tag_info = None
        title = u'讨论区'

    # topic list
    per_page = 10

    topic_model = TopicModel()
    current_page = toInt(params.get('page', 0))

    topic_list, count = topic_model.get_topic_list_and_count(
        where_obj,
        length=per_page,
        offset=current_page * per_page
    )

    # pager
    pager = widget.Pager(
        per_page=per_page,
        current_page=current_page,
        total_count=count
    )

    # uid
    uid = request.session.get('uid', -1)

    return frame.default_frame(
        request,
        {
            'tag_info': tag_info,
            'title': title,
            'pager': pager,
            'topic_list': topic_list,
            'timestr': datetime2Str,
            'avatar': avatarFunc(request),
            'uid': uid
        }
    )


def post_topic(request):
    ''' 发表主题的页面 '''
    return frame.default_frame(
        request,
        {
            'title': u'发表新主题'
        }
    )


@post_only
@frame.ajax_check_login
def ajax_post_topic(request, uid):
    ''' 发表主题的ajax接口 '''
    params = request.params()

    # validates
    result = validate_params(
        params,
        pick_dict(
            _common_validates,
            ('title', 'text')
        )
    )
    if result:
        return json_response({
            'result': 'failed',
            'msg': u'填写内容不符合要求',
            'validate_result': result,
        })

    # tags
    tags = Tags()
    tags.set_tag_list(params.get('tags', []))

    # validate tags
    res = tags.validate()
    if not res['result']:
        return json_response({
            'result': 'failed',
            'msg': res['msg']
        })

    # add topic to db
    tag_id_list = tags.idListInDb()
    add_new_topic(
        uid=uid,
        title=params.get('title', ''),
        text=params.get('text', ''),
        tag_id_list=tag_id_list
    )

    # response
    return json_response({
        'result': 'success',
        'msg': u'发表成功'
    })
