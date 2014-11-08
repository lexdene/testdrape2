# -*- coding: utf-8 -*-

import datetime

import drape
from drape.model import LinkedModel, F
from drape.util import toInt, pick_dict
from drape.response import json_response
from drape.validate import validate_params

from app.lib.text import datetime2Str, avatarFunc
from app.model.discuss import TopicModel, add_new_topic
from app.lib.tags import Tags

from .. import widget, frame


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
    params = request.params
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

        title = '标签: %s' % tag_info['content']

        where_obj = {
            'ttb.tag_id': tagid
        }
    else:
        tag_info = None
        title = '讨论区'

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


def new(request):
    ''' 发表主题的页面 '''
    return frame.default_frame(
        request,
        {
            'title': '发表新主题'
        }
    )


@frame.ajax_check_login
def create(request, uid):
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
            'msg': '填写内容不符合要求',
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
        'msg': '发表成功'
    })


def filter_topic(request):
    ''' 筛选主题的页面 '''
    return frame.default_frame(
        request,
        {
            'title': '筛选主题'
        }
    )


@frame.pager_ajax
def ajax_topic_list(request, page, per_page):
    # tag list
    params = request.params()
    where_obj = None
    tag_list = params.get('tags', [])
    if tag_list:
        where_obj = {
            'ttb.tag_id': (
                'in',
                [int(tag_id) for tag_id in tag_list]
            )
        }

    # read data from model
    topic_model = TopicModel()
    return topic_model.get_topic_list_and_count(
        where_obj,
        per_page,
        page * per_page
    )


def show(request):
    ''' 主题页面 '''
    params = request.params()
    topic_id = params['topic_id']

    # read topic info from model
    topic_model = LinkedModel('discuss_topic')
    topic_info = topic_model.alias(
        'topic'
    ).join(
        'userinfo',
        {'topic.uid': F('userinfo.id')}
    ).where({
        'topic.id': topic_id
    }).find()

    # error if not exist
    if topic_info is None:
        return frame.Error(request, '无此主题')

    # read reply list from model
    reply_model = LinkedModel('discuss_reply')
    reply_list = reply_model.alias(
        'reply'
    ).join(
        'userinfo',
        {'reply.uid': F('userinfo.id')}
    ).join(
        'discuss_reply',
        {'reply.reply_to_id': F('reply_to_reply.id')},
        'reply_to_reply'
    ).join(
        'userinfo',
        {'reply_to_reply.uid': F('reply_to_reply_userinfo.id')},
        'reply_to_reply_userinfo'
    ).where({
        'reply.tid': topic_id
    }).select()
    for floor, reply in enumerate(reply_list):
        reply['floor'] = floor + 1

    # read tag list from model
    tag_model = LinkedModel('tag')
    tag_list = tag_model.join(
        'discuss_topic_tag_bridge',
        {'bridge.tag_id': F('tag.id')},
        'bridge'
    ).where({
        'bridge.topic_id': topic_id
    }).select()

    # return frame
    return frame.default_frame(
        request,
        {
            'topicInfo': topic_info,
            'title': '%s - 讨论区' % topic_info['title'],
            'replyList': reply_list,
            'tagList': tag_list,
            'timestr': datetime2Str,
            'avatar': avatarFunc(request)
        }
    )
