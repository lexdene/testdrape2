# -*- coding: utf-8 -*-
'''
    与主题相关的controller
    版本: 2.0
'''

import time

from drape.controller import jsonController
from drape.model import LinkedModel
from drape.util import toInt

from .frame import DefaultFrame
from app.model.discuss import TopicModel

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
