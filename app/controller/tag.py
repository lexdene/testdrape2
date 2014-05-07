# -*- coding: utf-8 -*-
''' some controllers about tag '''
import random
from bisect import bisect_left

from drape.http import post_only
from drape.db import Db
from drape.model import LinkedModel, F
from drape.response import json_response
import drape.config
from drape.util import tile_list_data, toInt

from app.lib.cache import Cache, remove_cache
from . import frame


@post_only
def update_tag_cache(request):
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

    # clean up cache
    remove_cache('tag/hot_list')

    # 输出结果
    tag_model = LinkedModel('tag')
    tag_list = tag_model.join(
        'tag_cache',
        {'tag.id': F('tag_cache.id')},
        'tag_cache'
    ).order('tag_cache.reply_count', 'DESC').limit(50).select()

    return json_response({
        'tag_list': tag_list
    })


def get_hot_tag_list_from_db():
    ''' 从数据库中读取热门标签列表 '''
    tag_model = LinkedModel('tag')
    limit = drape.config.TAG_RANDOM_RANGE_LENGTH
    tag_list = tag_model.join(
        'tag_cache',
        {'tag.id': F('tag_cache.id')},
        'tag_cache'
    ).order(
        'tag_cache.reply_count', 'DESC'
    ).limit(limit).select()
    return tag_list


def random_tag_list(request):
    ''' 从最热门的标签中，随机选取标签列表 '''

    # 从缓存中读取热门标签列表
    cache = Cache()
    tag_list = cache.get('tag/hot_list', get_hot_tag_list_from_db)

    # 随机产生若干个
    result_list_length = 10
    result_list = list()
    random_key = 'tag_cache.reply_count'

    # 统计各个tag的权重之和
    tag_heavy_list = list()
    heavy = 0
    for tag in tag_list:
        if tag[random_key] is None:
            tag[random_key] = 1

        heavy += tag[random_key]
        tag_heavy_list.append(heavy)

    # 随机若干次，取出值
    random_tag_index_set = set()
    for _ in range(result_list_length):
        random_int = random.randint(0, heavy - 1)
        random_tag_index_set.add(
            bisect_left(
                tag_heavy_list, random_int
            )
        )

    # 标签列表
    result_tag_list = [
        tag_list[i] for i in random_tag_index_set
    ]

    # 按权重排序
    result_tag_list = sorted(
        result_tag_list,
        key=lambda tag: tag[random_key]
    )

    # 返回数据
    return json_response({
        'tag_list': tile_list_data(result_tag_list)
    })


def tag_list_page(request):
    ''' 全部标签的排行页面 '''
    return frame.default_frame(
        request,
        {
            'title': '全部标签'
        }
    )


@frame.pager_ajax
def ajax_tag_list(request, page, per_page):
    ''' ajax请求标签列表 '''
    # tag list
    tag_model = LinkedModel('tag')
    return tag_model.join(
        'tag_cache',
        {'cache.id': F('tag.id')},
        'cache'
    ).order(
        'cache.reply_count', 'DESC'
    ).order(
        'cache.topic_count', 'DESC'
    ).order(
        'id'
    ).limit(
        per_page
    ).offset(
        per_page * page
    ).select_and_count()
