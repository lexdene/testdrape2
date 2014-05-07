# -*- coding: utf-8 -*-

import re
import datetime

from drape.model import LinkedModel


class Tags(object):
    def __init__(self):
        self.__tagList = list()
        self.__separator = ' '

    def setTagString(self, tagString):
        tagList = tagString.split(self.__separator)

        # remove empty item
        tagList = [x for x in tagList if x != '']

        self.__tagList = tagList

    def set_tag_list(self, tag_list):
        self.__tagList = tag_list

    def validate(self):
        result = dict(
            result=True,
            msg='',
        )

        # is empty
        if len(self.tagList()) == 0:
            result['result'] = False
            result['msg'] = '标签不能为空'

        # 只能包含英文字母、数字、下划线、减号、井号
        reg = re.compile('^[-0-9a-zA-Z_#]+$')
        for tag in self.tagList():
            if not reg.match(tag):
                result['result'] = False
                result['msg'] = '只能包含英文字母、数字、下划线、减号、井号'
                result['debug'] = tag
                break

        return result

    def tagList(self):
        return self.__tagList

    def idListInDb(self):
        aTagModel = LinkedModel('tag')

        exist_tag_list = aTagModel.where(
            content=('in', self.tagList())
        ).select()

        not_exist_tag_list = set(self.tagList())

        for tag in exist_tag_list:
            not_exist_tag_list.remove(tag['content'])

        time_now = datetime.datetime.now()
        for tag_content in not_exist_tag_list:
            aTagModel.insert(
                content=tag_content,
                ctime=time_now
            )

        my_tag_list = aTagModel.where(
            content=('in', self.tagList())
        ).select()

        return [tag['id'] for tag in my_tag_list]

if '__main__' == __name__:
    tags = Tags()
    tags.setTagString('')
    print(tags.tagList())

    tags.setTagString('  a  b  c  ')
    print(tags.tagList())
