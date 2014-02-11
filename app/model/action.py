from drape.model import LinkedModel, F


class ActionModel(LinkedModel):
    def __init__(self):
        super(ActionModel, self).__init__('action')

    def getList(self, where, from_id):
        # from id
        if from_id > 0:
            where['action.id'] = ('<', from_id)

        action_list = self.join(
            'focus',
            {
                'focus.focus_type': F('action.from_object_type'),
                'focus.target_id': F('action.from_object_id'),
                'focus.is_del': 0
            },
            'focus'
        ).where(
            where
        ).group(
            'action.id'
        ).order(
            'action.id', 'DESC'
        ).limit(10).select()

        topic_model = LinkedModel('discuss_topic')
        userinfo_model = LinkedModel('userinfo')
        reply_model = LinkedModel('discuss_reply')
        tag_model = LinkedModel('tag')

        # from/target object
        def get_topic_info(id):
            return topic_model.where(id=id).find()

        def get_user_info(id):
            return userinfo_model.where(id=id).find()

        def get_reply_info(id):
            return reply_model.alias('reply').where({'reply.id': id}).join(
                'discuss_topic', 'topic', 'reply.tid=topic.id'
                ).find()

        def get_tag_info(id):
            return tag_model.where(id=id).find()

        model_map = {
            'topic': get_topic_info,
            'user': get_user_info,
            'reply': get_reply_info,
            'tag': get_tag_info
        }
        for field in ('from', 'target'):
            for action in action_list:
                object_type = action['%s_object_type' % field]
                get_info = model_map[object_type]

                info_key = '%s_%s_info' % (field, object_type)
                action[info_key] = get_info(action['%s_object_id' % field])

        return action_list
