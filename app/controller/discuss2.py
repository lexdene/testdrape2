# -*- coding: utf-8 -*-
'''
    与主题相关的controller
    版本: 2.0
'''

import datetime

from drape.controller import JsonController, post_only
from drape.model import LinkedModel
from drape.util import toInt
from drape.validate import validate_params

from .frame import DefaultFrame
from app.lib.login import check_login, ajax_check_login
from app.model.discuss import TopicModel, add_new_topic
from app.lib.tags import Tags

DEFAULT_CLS = 'filter_topic'


@DefaultFrame.controller
def filter_topic(self):
    ''' 筛选主题的页面 '''
    self.setTitle(u'筛选主题')


@JsonController.controller
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
    self.set_variable('page', page)
    self.set_variable('per_page', per_page)

    # tag list
    tag_model = LinkedModel('tag')
    tag_list = tag_model.limit(
        per_page,
        per_page * page
    ).select(['SQL_CALC_FOUND_ROWS'])
    self.set_variable('tag_list', tag_list)

    # count
    count = tag_model.found_rows()
    self.set_variable('total_count', count)


@JsonController.controller
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
    self.set_variable('now', datetime.datetime.now())

    # page
    params = self.params()
    per_page = 10
    page = toInt(params.get('page', 0))
    self.set_variable('page', page)
    self.set_variable('per_page', per_page)

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
    self.set_variable('topic_list', topic_list)
    self.set_variable('total_count', count)


@DefaultFrame.controller
@check_login
def post_topic(self):
    ''' 发表主题的页面 '''
    self.setTitle(u'发表新主题')


@JsonController.controller
@post_only
@ajax_check_login
def ajax_post_topic(self):
    ''' 发表主题的ajax接口 '''
    params = self.params()
    for key, value in params.iteritems():
        self.set_variable(key, value)

    session = self.session()
    uid = toInt(session.get('uid', -1))

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
        self.set_variable('result', 'failed')
        self.set_variable('msg', res['msg'])
        return

    # tags
    tags = Tags()
    tags.set_tag_list(params.get('tags', []))

    # validate tags
    res = tags.validate()
    if False == res['result']:
        self.set_variable('result', 'failed')
        self.set_variable('msg', res['msg'])
        return

    # get tag id list
    tag_id_list = tags.idListInDb()

    # add topic to db
    add_new_topic(
        uid=uid,
        title=params.get('title', ''),
        text=params.get('text', ''),
        tag_id_list=tag_id_list
    )

    self.set_variable('result', 'success')
    self.set_variable('msg', u'发表成功')
