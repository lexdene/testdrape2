# -*- coding: utf-8 -*-
'''
    首页
    各种动态
'''

from os import listdir
from os.path import isfile, join
import re

from . import frame

DEFAULT_CLS = 'DateList'


class DateList(frame.DefaultFrame):
    '''
        日志的日期列表
    '''
    def process(self):
        self.setTitle('日期列表 - 查看日志')

        log_dir_path = 'data/log'
        datelist = [f.split('.')[0] for f in listdir(log_dir_path)]
        datelist.sort(reverse=True)
        self.set_variable('datelist', datelist)


class Content(frame.DefaultFrame):
    '''
        日志的内容
    '''
    def process(self):
        self.setTitle('日志内容 - 查看日志')

        params = self.params()
        date = params.get('date', '')

        file_path = 'data/log/%s.log' % date
        datalist = list()
        r = re.compile(
            r'\[(?P<time>[-0-9 :,]*)\] \[(?P<type>[A-Z]*)\] (?P<content>.*)'
        )
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                m = r.match(line)
                datalist.append({
                    'n': i,
                    'time': m.group('time'),
                    'type': m.group('type'),
                    'content': re.sub(r'\\n', '\n', m.group('content'))
                })
        self.set_variable('datalist', datalist[-100:])
