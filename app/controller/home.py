# -*- coding: utf-8 -*-
'''
    首页
    各种动态
'''

import datetime

from drape.controller import JsonController
from drape.util import toInt
from drape.model import LinkedModel

from . import frame
from app.model.action import ActionModel

DEFAULT_CLS = 'HomeLine'


class HomeLine(frame.DefaultFrame):
    '''
        只是显示个页面，没有实际数据。
        数据通过ajax请求。
    '''
    def process(self):
        self.setTitle(u'首页')


class AjaxHomeLine(JsonController):
    '''
        HomeLine的数据
    '''
    def process(self):
        # get uid from session
        aSession = self.session()
        uid = toInt(aSession.get('uid', -1))

        # from id
        aParams = self.params()
        from_id = toInt(aParams.get('from_id', 0))

        # get data from db
        action_model = ActionModel()
        action_list = action_model.getList(
            {
                '$or': (
                    {'focus.from_uid': uid},
                    {
                        'action.from_object_type': 'user',
                        'action.from_object_id': uid
                    }
                )
            },
            from_id
        )
        self.set_variable('data', action_list)

        # now
        now = datetime.datetime.now()
        self.set_variable('now', now)

        # error msg
        self.set_variable('errormsg', '')
