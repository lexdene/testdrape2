# -*- coding: utf-8 -*-
''' 与用户留言板相关的后台接口 '''

import datetime

from drape.controller import JsonController
from drape.util import toInt, tile_list_data
from drape.validate import validate_params
from drape.model import LinkedModel

from app.lib.cache import remove_cache
from .frame import DefaultFrame

class AjaxPostMsg(JsonController):
    ''' 发表留言 '''
    def process(self):
        # get uid from session
        session = self.session()
        my_uid = toInt(session.get('uid', -1))
        if my_uid < 0:
            self.set_variable('result', 'failed')
            self.set_variable('msg', '请先登录')
            return

        # validate
        params = self.params()
        res = validate_params(
            params,
            [
                {
                    'key': 'to_uid',
                    'name': '目标用户',
                    'validates': [
                        ('int', ),
                    ]
                },
                {
                    'key': 'text',
                    'name': '内容',
                    'validates': [
                        ('notempty', ),
                        ('len', 1, 200)
                    ]
                }
            ]
        )
        if False == res['result']:
            self.set_variable('result', 'failed')
            self.set_variable('msg', res['msg'])
            return

        # params
        to_uid = toInt(params.get('to_uid', -1))
        text = params.get('text', '')
        now = datetime.datetime.now()

        # insert to db
        usermsg_model = LinkedModel('usermsg')
        usermsg_id = usermsg_model.insert(
            from_uid=my_uid,
            to_uid=to_uid,
            text=text,
            ctime=now
        )

        # notice
        notice_model = LinkedModel('notice')
        notice_model.insert(
            from_uid=my_uid,
            to_uid=to_uid,
            item_id=usermsg_id,
            type='usermsg',
            ctime=now,
            isRead=False
        )
        remove_cache('notice_count/%s' % to_uid)

        # result
        self.set_variable('result', 'success')
        self.set_variable('msg', '留言成功')


class AjaxMsgList(JsonController):
    ''' 留言列表
        返回值格式
        {
            'now':          # 服务器当前时间
            'errormsg':     # 错误原因，成功时为空
            'per_page':     # 每页几条
            'page':         # 当前第几页
            'count':        # 一共有几条
            'data': [       # 数据
            ]
        }
    '''
    def process(self):
        # now
        now = datetime.datetime.now()
        self.set_variable('now', now)

        # page
        params = self.params()
        per_page = 10
        page = toInt(params.get('page', 0))
        self.set_variable('per_page', per_page)
        self.set_variable('page', page)

        # my uid
        session = self.session()
        my_uid = toInt(session.get('uid', -1))
        if my_uid < 0:
            self.set_variable('errormsg', '未登录用户无法查看留言板')
            self.set_variable('data', [])
            return

        # to uid
        to_uid = toInt(params.get('to_uid', -1))
        where_data = {}
        if to_uid < 0 or to_uid == my_uid:
            where_data = {
                '$or': (
                    {
                        'from_uid': my_uid,
                    },
                    {
                        'to_uid': my_uid,
                    }
                )
            }
        else:
            where_data = {
                '$or': (
                    {
                        'from_uid': my_uid,
                        'to_uid': to_uid,
                    },
                    {
                        'from_uid': to_uid,
                        'to_uid': my_uid,
                    }
                )
            }

        self.set_variable('errormsg', '')

        usermsg_model = LinkedModel('usermsg')
        usermsg_list = usermsg_model.join(
            'userinfo', 'from_ui',
            'from_ui.id=usermsg.from_uid'
        ).join(
            'userinfo', 'to_ui',
            'to_ui.id=usermsg.to_uid'
        ).where(where_data).limit(
            per_page,
            per_page * page
        ).order('usermsg.ctime', 'DESC').select(['SQL_CALC_FOUND_ROWS'])
        self.set_variable('data', tile_list_data(usermsg_list))

        # count
        self.set_variable('count', usermsg_model.found_rows())


@DefaultFrame.controller
def MyMsgList(self):
    self.setTitle('我的留言板')
