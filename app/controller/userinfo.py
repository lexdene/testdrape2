# -*- coding: utf-8 -*-

import datetime

import drape
from drape.util import tile_list_data

import frame
import app.lib.text
from app.model.discuss import TopicModel
from focus import isFocused
from app.model.action import ActionModel

def avatarFunc(controller):
	root = controller.runbox().request().rootPath()
	def avatar(a):
		return a if a else root+'/static/image/avatar.jpg'
	return avatar

class MainPage(frame.DefaultFrame):
	def process(self):
		aParams = self.params()
		uid = drape.util.toInt(aParams.get('id',-1))
		if uid < 0:
			self.Error(u'参数无效:id格式非法')
			return
		
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		userinfo = aUserinfoModel.where(id=uid).find()
		if userinfo is None:
			self.Error(u'无此用户')
			return
		
		self.setTitle(userinfo['nickname'])
		self.set_variable('userinfo', userinfo)
		self.set_variable('timestr', app.lib.text.datetime2Str)
		self.set_variable('avatar', avatarFunc(self))
		self.set_variable('isFocused', isFocused(self, 'user', uid))


class UserTopicList(frame.FrameBase):
	def process(self):
		aParams = self.params()
		uid = drape.util.toInt(aParams.get('uid',-1))
		if uid < 0:
			self.Error(u'参数无效:id格式非法')
			return
		
		aTopicModel = TopicModel()
		arrTopicList = aTopicModel.getTopicList(uid = uid)
		
		self.set_variable('topic_list',arrTopicList)
		self.set_variable(
			'avatar',
			avatarFunc(self)
		)
		self.set_variable('timestr', app.lib.text.datetime2Str)
		self.set_variable('show_user_info', False )


class ajaxUserActionList(drape.controller.JsonController):
	'''
	返回值格式：
	{
		'now': # 服务器当前时间
		'errormsg': # 错误原因,成功时为空
		'data': [ # 数据
		]
	}
	'''
	def process(self):
		# now
		now = datetime.datetime.now()
		self.set_variable('now', now)

		aParams = self.params()
		uid = drape.util.toInt(aParams.get('uid', -1))
		if uid < 0:
			self.set_variable('errormsg', u'uid参数错误')
			self.set_variable('data', [])
		else:
			self.set_variable('errormsg', '')

			from_id = drape.util.toInt(aParams.get('from_id', 0))
			action_model = ActionModel()
			action_list = action_model.getList({
				'from_object_id': uid,
				'from_object_type': 'user'
			}, from_id)
			self.set_variable('data', tile_list_data(action_list))
