# -*- coding: utf-8 -*-
'''
    首页
    各种动态
'''

import time

from drape.controller import jsonController
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


class AjaxHomeLine(jsonController):
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
        action_list = action_model.getList({'focus.from_uid': uid}, from_id)
        self.setVariable('data', action_list)

        # now
        now = int(time.time())
        self.setVariable('now', now)

        # error msg
        self.setVariable('errormsg', '')
