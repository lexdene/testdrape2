import drape

class TopicModel(drape.model.LinkedModel):
    def __init__(self):
        super(TopicModel,self).__init__('discuss_topic')

    def getTopicList(self, uid=None, length=10, offset=0):
        where_obj = dict()
        
        # uid
        if uid :
            where_obj['dt.uid'] = uid

        aTopicList = self \
            .alias('dt') \
            .join('userinfo','topic_ui','dt.uid = topic_ui.id') \
            .join('discuss_topic_cache','tc','tc.id = dt.id') \
            .join('discuss_reply','last_reply','last_reply.id = tc.last_reply_id') \
            .join('userinfo','last_reply_ui','last_reply.uid = last_reply_ui.id') \
            .join('discuss_reply','count_dr','count_dr.tid = dt.id') \
            .join('discuss_topic_tag_bridge','ttb','ttb.topic_id = dt.id') \
            .join('tag','tag','tag.id = ttb.tag_id') \
            .field('COUNT(DISTINCT count_dr.id) as reply_count') \
            .field('GROUP_CONCAT(tag.content) as tags') \
            .order('CASE WHEN last_reply.id is NULL THEN dt.ctime ELSE last_reply.ctime END DESC') \
            .group('dt.id') \
            .reflectField(True) \
            .limit(length,offset) \
            .where(where_obj) \
            .select()
        
        # filter tags
        for topic in aTopicList:
            if topic['tags'] is None:
                topic['tag_list'] = list()
            else:
                topic['tag_list'] = topic['tags'].split(',')

        return aTopicList
