# -*- coding: utf-8 -*-
'''
    首页
    各种动态
'''

import datetime

from drape.util import toInt, tile_list_data
from drape.response import json_response

from . import frame
from app.model.action import ActionModel

DEFAULT_CONTROLLER = 'HomeLine'


def index(request):
    '''
        只是显示个页面, 没有实际数据.
        数据通过ajax请求.
    '''
    accept = request.chief_accept()
    if accept == 'application/json':
        return AjaxHomeLine(request)
    else:
        return frame.default_frame(
            request,
            {
                'title': '新鲜事',
            }
        )


def AjaxHomeLine(request):
    '''
        HomeLine的数据
        参数from_id用来翻页
    '''
    # uid
    uid = toInt(request.session.get('uid', 0))

    # from id
    params = request.params()
    from_id = toInt(params.get('from_id', 0))

    # get data from db
    action_model = ActionModel()
    action_list = action_model.getList(
        {
            '__or': (
                {'focus.from_uid': uid},
                {
                    'action.from_object_type': 'user',
                    'action.from_object_id': uid
                }
            )
        },
        from_id
    )

    return json_response(tile_list_data(action_list))
