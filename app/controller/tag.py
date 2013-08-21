# -*- coding: utf-8 -*-
''' some controllers about tag '''
import random

from drape.controller import jsonController
from drape.db import Db
from drape.model import LinkedModel
from drape.config import get_value as config_value
from drape.util import tile_list_data, toInt

from .frame import DefaultFrame


@jsonController.controller
def update_tag_cache(self):
    ''' 更新tag_cache表 '''
    db_object = Db()

    # 更新topic_count和reply_count
    db_object.execute('''
        REPLACE INTO {prefix}tag_cache (id, topic_count, reply_count)
        SELECT tag.id,
        (
            SELECT COUNT( dt.id ) from {prefix}discuss_topic as dt
            LEFT JOIN {prefix}discuss_topic_tag_bridge as ttb
                on ttb.topic_id = dt.id
            WHERE ttb.tag_id = tag.id
        ),
        (
            SELECT COUNT( re.id ) from {prefix}discuss_reply as re
            LEFT JOIN {prefix}discuss_topic_tag_bridge as ttb
                on ttb.topic_id = re.tid
            WHERE ttb.tag_id = tag.id
        )
        FROM {prefix}tag as tag'''.format(
            prefix=db_object.table_prefix()
        )
    )

    # 输出结果
    tag_model = LinkedModel('tag')
    tag_list = tag_model.join(
        'tag_cache', 'tag_cache', 'tag.id = tag_cache.id'
    ).order('tag_cache.reply_count', 'DESC').limit(50).select()

    self.setVariable('tag_list', tag_list)


@jsonController.controller
def random_tag_list(self):
    ''' 从最热门的标签中，随机选取标签列表 '''
    tag_model = LinkedModel('tag')
    limit = config_value('tag/random_range_length')
    tag_list = tag_model.join(
        'tag_cache', 'tag_cache', 'tag.id = tag_cache.id'
    ).order('tag_cache.reply_count', 'DESC').limit(limit).select()

    result_list_length = 10
    result_list = list()
    random_key = 'tag_cache.reply_count'
    for _ in range(result_list_length):
        random_top = 0
        for tag in tag_list:
            if tag.get('enable', True):
                random_top += tag[random_key]

        n_random = random.randint(0, random_top - 1)
        random_top = 0
        for tag in tag_list:
            if tag.get('enable', True):
                random_top += tag[random_key]

            if random_top >= n_random:
                result_list.append(tag)
                tag['enable'] = False
                break

    self.setVariable('tag_list', tile_list_data(result_list))


@DefaultFrame.controller
def tag_list_page(self):
    ''' 全部标签的排行页面 '''
    self.setTitle(u'全部标签')


@jsonController.controller
def ajax_tag_list(self):
    ''' ajax请求标签列表 '''
    # page
    params = self.params()
    per_page = 20
    page = toInt(params.get('page', 0))
    self.setVariable('page', page)
    self.setVariable('per_page', per_page)

    # tag list
    tag_model = LinkedModel('tag')
    tag_list = tag_model.join(
        'tag_cache', 'cache', 'cache.id = tag.id'
    ).order(
        'cache.reply_count', 'DESC'
    ).order(
        'cache.topic_count', 'DESC'
    ).order(
        'id'
    ).limit(
        per_page,
        per_page * page
    ).select(['SQL_CALC_FOUND_ROWS'])
    self.setVariable('tag_list', tile_list_data(tag_list))

    # count
    count = tag_model.found_rows()
    self.setVariable('total_count', count)
