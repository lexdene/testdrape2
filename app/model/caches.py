'some cache by functions'
from drape.model import LinkedModel, F

from app.lib.cache import cache_by


@cache_by('userinfo/{0}')
def get_userinfo(uid):
    'userinfo by uid'
    return LinkedModel(
        'userinfo'
    ).where(
        id=uid
    ).find()


@cache_by('notice_count/{0}')
def get_notice_count(uid):
    'notice count by uid'
    return LinkedModel(
        'notice'
    ).where(
        to_uid=uid,
        isRead=0
    ).count()


@cache_by('mail_count/{0}')
def get_mail_count(uid):
    'mail count by uid'
    return LinkedModel(
        'mail'
    ).where(
        to_uid=uid,
        isRead=0
    ).count()

@cache_by('topic_info/{0}')
def get_topic_info(topic_id):
    topic_model = LinkedModel('discuss_topic')

    topic = topic_model.alias(
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
