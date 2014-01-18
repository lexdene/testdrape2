# -*- coding: utf-8 -*-

import datetime

import drape
from drape.model import LinkedModel
from drape.util import toInt

from app.lib.text import datetime2Str, avatarFunc
from app.model.discuss import TopicModel

from . import widget, frame

DEFAULT_CONTROLLER = 'List'


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
