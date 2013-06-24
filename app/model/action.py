from drape.model import LinkedModel


class ActionModel(LinkedModel):
    def __init__(self):
        super(ActionModel, self).__init__('action')

    def getList(self, where, from_id):
        # from id
        if from_id > 0:
            where['action.id'] = ('<', from_id)

        action_list = self.join(
            'focus',
            'focus',
            'focus.focus_type = action.from_object_type'
            + ' AND focus.target_id = action.from_object_id'
        ).where(where).group('action.id').order('action.id DESC').limit(10).select()

        topic_model = LinkedModel('discuss_topic')
        userinfo_model = LinkedModel('userinfo')

        # from/target object
        model_map = {
            'topic': topic_model,
            'user': userinfo_model
        }
        for field in ('from', 'target'):
            for action in action_list:
                object_type = action['%s_object_type' % field]
                info_model = model_map[object_type]

                info_key = '%s_%s_info' % (field, object_type)
                action[info_key] = info_model.where(
                    id=action['%s_object_id' % field]
                ).find()

        return action_list
