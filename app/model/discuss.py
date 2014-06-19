# -*- coding: utf-8 -*-
import datetime

import drape
from drape.model import LinkedModel, F

from app.lib.cache import cache_by


class TopicModel(drape.model.LinkedModel):
    def __init__(self):
        super(TopicModel, self).__init__('discuss_topic')

    def getTopicCount(self, uid=None, tagid=None):
        where_obj = dict()

        # uid
        if uid:
            where_obj['dt.uid'] = drape.util.toInt(uid)
        # tag id
        if tagid:
            where_obj['ttb.tag_id'] = drape.util.toInt(tagid)

        count = self.alias(
            'dt'
        ).join(
            'discuss_topic_tag_bridge', 'ttb', 'ttb.topic_id = dt.id'
        ).where(
            where_obj
        ).count('DISTINCT dt.id')
        return count

    def getTopicList(self, uid=None, tagid=None, length=10, offset=0):
        where_obj = dict()

        # uid
        if uid:
            where_obj['dt.uid'] = uid

        # tag id
        if tagid:
            where_obj['ttb.tag_id'] = tagid

        aTopicList = self.alias(
            'dt'
        ).join(
            'userinfo', 'topic_ui', 'dt.uid = topic_ui.id'
        ).join(
            'discuss_topic_cache', 'tc', 'tc.id = dt.id'
        ).join(
            'discuss_reply', 'last_reply', 'last_reply.id = tc.last_reply_id'
        ).join(
            'userinfo', 'last_reply_ui', 'last_reply.uid = last_reply_ui.id'
        ).join(
            'discuss_reply', 'count_dr', 'count_dr.tid = dt.id'
        ).join(
            'discuss_topic_tag_bridge', 'ttb', 'ttb.topic_id = dt.id'
        ).field(
            'COUNT(DISTINCT count_dr.id) as reply_count'
        ).order(
            'last_reply.ctime', 'DESC'
        ).order(
            'id'
        ).group(
            'dt.id'
        ).limit(
            length, offset
        ).where(
            where_obj
        ).select()

        # filter tags
        aTagModel = drape.model.LinkedModel('tag')
        for topic in aTopicList:
            topic['tag_list'] = aTagModel.join(
                'discuss_topic_tag_bridge', 'ttb', 'ttb.tag_id = tag.id'
            ).where({
                'ttb.topic_id': topic['id']
            }).select()

        return aTopicList

    def get_topic_list_and_count(self, where_obj=None, length=10, offset=0):
        '''
            where_obj只支持查询作者和标签
            length和offset是limit参数

            返回主题列表和总数
        '''
        self.alias('dt').join(
            'discuss_topic_cache',
            {
                'tc.id': F('dt.id')
            },
            'tc',
        ).join(
            'discuss_reply',
            {
                'last_reply.id': F('tc.last_reply_id')
            },
            'last_reply',
        ).join(
            'discuss_topic_tag_bridge',
            {
                'ttb.topic_id': F('dt.id')
            },
            'ttb',
        ).order(
            'last_reply.ctime',  self.DESC
        ).order(
            'id'
        ).group(
            'dt.id'
        ).limit(
            length
        ).offset(
            offset
        )

        if where_obj:
            self.where(where_obj)

        topic_list, count = self.select_and_count()

        # filter tags
        for topic in topic_list:
            topic_info = self.get_topic_info(topic['id'])
            for key, value in topic_info.items():
                if key not in topic:
                    topic[key] = value

        return topic_list, count

    @cache_by('topic_info/{1}')
    def get_topic_info(self, topic_id):
        topic = self.alias(
            'dt'
        ).join(
            'userinfo',
            {
                'dt.uid': F('topic_ui.id')
            },
            'topic_ui'
        ).join(
            'discuss_topic_cache',
            {
                'tc.id': F('dt.id')
            },
            'tc'
        ).join(
            'discuss_reply',
            {
                'last_reply.id': F('tc.last_reply_id')
            },
            'last_reply'
        ).join(
            'userinfo',
            {
                'last_reply.uid': F('last_reply_ui.id')
            },
            'last_reply_ui',
        ).join(
            'discuss_reply',
            {
                'count_dr.tid': F('dt.id')
            },
            'count_dr'
        ).where({
            'dt.id': topic_id
        }).find(
            ['COUNT(DISTINCT count_dr.id) as reply_count']
        )

        tag_model = LinkedModel('tag')
        topic['tag_list'] = tag_model.join(
            'discuss_topic_tag_bridge',
            {
                'ttb.tag_id': F('tag.id')
            },
            'ttb'
        ).where({
            'ttb.topic_id': topic['id']
        }).select()

        return topic


def add_new_topic(uid, title, text, tag_id_list):
    # now
    now = datetime.datetime.now()

    # insert topic
    discuss_model = LinkedModel('discuss_topic')
    topicid = discuss_model.insert(
        uid=uid,
        ctime=now,
        title=title,
    )

    # insert reply
    replyid = LinkedModel('discuss_reply').insert(
        tid=topicid,
        uid=uid,
        reply_to_id=-1,
        ctime=now,
        text=text,
    )

    # topic cache
    LinkedModel('discuss_topic_cache').insert(
        id=topicid,
        first_reply_id=replyid,
        last_reply_id=replyid
    )

    # topic tag bridge
    bridge_model = LinkedModel('discuss_topic_tag_bridge')
    for tag_id in tag_id_list:
        bridge_model.insert(
            tag_id=tag_id,
            topic_id=topicid
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
    for tag_id in tag_id_list:
        action_model.insert(
            from_object_id=tag_id,
            from_object_type='tag',
            action_type='post',
            target_object_id=topicid,
            target_object_type='topic',
            ctime=now
        )
