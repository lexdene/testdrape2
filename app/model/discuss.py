import time

import drape
from drape.model import LinkedModel


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
        self.alias('dt').join(
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
            'last_reply.ctime',  'DESC'
        ).order(
            'id'
        ).group(
            'dt.id'
        ).limit(
            length, offset
        )

        if where_obj:
            self.where(where_obj)

        topic_list = self.select(['SQL_CALC_FOUND_ROWS'])
        count = self.found_rows()

        # filter tags
        tag_model = drape.model.LinkedModel('tag')
        for topic in topic_list:
            topic['tag_list'] = tag_model.join(
                'discuss_topic_tag_bridge', 'ttb', 'ttb.tag_id = tag.id'
            ).where({
                'ttb.topic_id': topic['id']
            }).select()

        return topic_list, count


def add_new_topic(uid, title, text, tag_id_list):
    # now
    now = int(time.time())

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
