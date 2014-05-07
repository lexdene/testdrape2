# -*- coding: utf-8 -*-
'''
    与用户信息相关的controller
    版本: 2.0
'''
import datetime

from drape.controller import JsonController
from drape.util import toInt
from drape.model import LinkedModel
from app.model.discuss import TopicModel


@JsonController.controller
def ajax_user_info(self):
    ''' 用户资料 '''
    # uid
    params = self.params()
    uid = toInt(params.get('uid'), -1)
    self.set_variable('uid', uid)

    # user info
    userinfo_model = LinkedModel('userinfo')
    userinfo = userinfo_model.where(id=uid).find()
    if userinfo is None:
        self.set_variable('result', 'failed')
        self.set_variable('msg', '无此用户')
        return

    # ctime
    userinfo['ctime'] = userinfo['ctime'].strftime('%Y-%m-%d')

    # topic count
    topic_model = LinkedModel('discuss_topic')
    userinfo['topic_count'] = topic_model.where(uid=uid).count()

    # reply count
    reply_model = LinkedModel('discuss_reply')
    userinfo['reply_count'] = reply_model.where(uid=uid).count()

    # set variable
    self.set_variable('result', 'success')
    self.set_variable('userinfo', userinfo)


@JsonController.controller
def ajax_user_topic_list(self):
    ''' 获取某用户发过的文章列表 '''
    params = self.params()
    uid = toInt(params.get('uid', -1))

    topic_model = TopicModel()
    topic_list, count = topic_model.get_topic_list_and_count(
        where_obj={
            'dt.uid': uid
        }
    )

    self.set_variable('result', 'success')
    self.set_variable('topic_list', topic_list)
    self.set_variable('count', count)

    # now
    self.set_variable('now', datetime.datetime.now())
