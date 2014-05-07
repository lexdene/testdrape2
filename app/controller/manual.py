# -*- coding: utf-8 -*-
''' 手册相关页面 '''

from . import frame

from app.lib.render import markdown


class ManualFrame(frame.FrameBase):
    ''' 页面结构 '''
    def __init__(self, path):
        super(ManualFrame, self).__init__(path)
        self._set_parent('manual/Layout')

    def set_sub_title(self, title):
        ''' 设置子标题 '''
        self.runbox().variables()['subtitle'] = title

    def render(self, template_path, variables):
        return markdown(
            template_path,
            variables
        )


class Layout(frame.DefaultFrame):
    ''' 布局 '''
    def process(self):
        subtitle = self.runbox().variables().get('subtitle')
        self.set_variable('subtitle', subtitle)
        self.setTitle('%s - drape开发手册' % subtitle)


class Index(ManualFrame):
    ''' 简介 '''
    def process(self):
        self.set_sub_title('简介')


class Mvc(ManualFrame):
    ''' MVC '''
    def process(self):
        self.set_sub_title('MVC')


class MvcController(ManualFrame):
    ''' MVC/Controller '''
    def process(self):
        self.set_sub_title('MVC/Controller')


class MvcModel(ManualFrame):
    ''' MVC/Model '''
    def process(self):
        self.set_sub_title('MVC/Model')


class MvcView(ManualFrame):
    ''' MVC/View '''
    def process(self):
        self.set_sub_title('MVC/View')
