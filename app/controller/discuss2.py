# -*- coding: utf-8 -*-
'''
    与主题相关的controller
    版本: 2.0
'''

import time

from drape.controller import jsonController
from drape.model import LinkedModel
from drape.util import toInt
from drape.validate import validate_params

from .frame import DefaultFrame
from app.model.discuss import TopicModel
from app.lib.tags import Tags

DEFAULT_CLS = 'filter_topic'


@DefaultFrame.controller
def filter_topic(self):
    ''' 筛选主题的页面 '''
    self.setTitle(u'筛选主题')


@jsonController.controller
def ajax_tag_list(self):
    '''
    返回值格式
        page
        per_page
        total_count
        tag_list
    '''
    # page
    params = self.params()
    per_page = 20
    page = toInt(params.get('page', 0))
    self.setVariable('page', page)
    self.setVariable('per_page', per_page)

    # tag list
    tag_model = LinkedModel('tag')
    tag_list = tag_model.limit(
        per_page,
        per_page * page
    ).select(['SQL_CALC_FOUND_ROWS'])
    self.setVariable('tag_list', tag_list)

    # count
    count = tag_model.found_rows()
    self.setVariable('total_count', count)


@jsonController.controller
def ajax_topic_list(self):
    '''
    参数
        page
        tag_list
    返回值格式
        page
        per_page
        total_count
        topic_list
    '''
    # now
    self.setVariable('now', int(time.time()))

    # page
    params = self.params()
    per_page = 10
    page = toInt(params.get('page', 0))
    self.setVariable('page', page)
    self.setVariable('per_page', per_page)

    # tag_list
    where_obj = None
    tag_list = params.get('tag_list', '')
    if tag_list:
        where_obj = {
            'ttb.tag_id': (
                'in',
                [int(tag_id) for tag_id in tag_list.split(',')])
        }

    topic_model = TopicModel()
    topic_list, count = topic_model.get_topic_list_and_count(
        where_obj, per_page, page * per_page
    )
    self.setVariable('topic_list', topic_list)
    self.setVariable('total_count', count)


@DefaultFrame.controller
def post_topic(self):
    ''' 发表主题的页面 '''
    self.setTitle(u'发表新主题')


@jsonController.controller
def ajax_post_topic(self):
    ''' 发表主题的ajax接口 '''
    params = self.params()
    for key, value in params.iteritems():
        self.setVariable(key, value)

    session = self.session()
    uid = toInt(session.get('uid', -1))
    if uid < 0:
        self.setVariable('result', 'failed')
        self.setVariable('msg', u'请先登录')
        return

    # validates
    validates = [
        dict(
            key='title',
            name=u'标题',
            validates=[
                ('notempty',),
                ('len', 4, 50)
            ]
        ),
        dict(
            key='text',
            name=u'内容',
            validates=[
                ('notempty',),
                ('len', 4, 500)
            ]
        ),
    ]
    res = validate_params(params, validates)
    if False == res['result']:
        self.setVariable('result', 'failed')
        self.setVariable('msg', res['msg'])
        return

    # tags
    tags = Tags()
    tags.set_tag_list(params.get('tags', []))

    # validate tags
    res = tags.validate()
    if False == res['result']:
        self.setVariable('result', 'failed')
        self.setVariable('msg', res['msg'])
        return

    # get tag id list
    tag_id_list = tags.idListInDb()

    # now
    now = int(time.time())

    # insert topic
    discuss_model = LinkedModel('discuss_topic')
    topicid = discuss_model.insert(
        uid=uid,
        ctime=now,
        title=params.get('title', ''),
    )

    # insert reply
    replyid = LinkedModel('discuss_reply').insert(
        tid=topicid,
        uid=uid,
        reply_to_id=-1,
        ctime=now,
        text=params.get('text', '')
    )

    # topic cache
    LinkedModel('discuss_topic_cache').insert(
        id=topicid,
        first_reply_id=replyid,
        last_reply_id=replyid
    )

    # topic tag bridge
    LinkedModel('discuss_topic_tag_bridge').insert(
        tag_id=tag_id_list,
        topic_id=[topicid] * len(tag_id_list)
    )

    # action
    # user post topic
    action_model = LinkedModel('action')
    action_model.insert(
        from_object_id=uid,
        from_object_type='user',
        action_type='post',
        target_object_id=topicid,
        target_object_type='topic',
        ctime=now
    )

    # tag post topic
    action_model.insert(
        from_object_id=tag_id_list,
        from_object_type='tag',
        action_type='post',
        target_object_id=topicid,
        target_object_type='topic',
        ctime=now
    )

    self.setVariable('result', 'success')
    self.setVariable('msg', u'发表成功')
