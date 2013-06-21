# -*- coding: utf-8 -*-

import time

import drape

import frame
import app.lib.text
from app.model.discuss import TopicModel
from focus import isFocused

def avatarFunc(root):
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
		self.setVariable('userinfo', userinfo)
		self.setVariable('timestr', app.lib.text.timeStamp2Str)
		self.setVariable('avatar', avatarFunc(self.request().rootPath()))
		self.setVariable('isFocused', isFocused(self, 'user', uid))


class UserPanelPage(frame.FrameBase):
	def process(self):
		aParams = self.params()
		uid = drape.util.toInt(aParams.get('uid',-1))
		if uid < 0:
			self.Error(u'参数无效:id格式非法')
			return
		
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		userinfo = aUserinfoModel.where(id=uid).find()
		if userinfo is None:
			self.Error(u'无此用户')
			return
		
		self.setVariable('userinfo',userinfo)
		self.setVariable('avatar',avatarFunc(self.request().rootPath()) )
		self.setVariable('timestr',app.lib.text.timeStamp2Str)

class UserTopicList(frame.FrameBase):
	def process(self):
		aParams = self.params()
		uid = drape.util.toInt(aParams.get('uid',-1))
		if uid < 0:
			self.Error(u'参数无效:id格式非法')
			return
		
		aTopicModel = TopicModel()
		arrTopicList = aTopicModel.getTopicList(uid = uid)
		
		self.setVariable('topic_list',arrTopicList)
		self.setVariable('timestr',app.lib.text.timeStamp2Short)
		self.setVariable('show_user_info', False )


class ajaxUserActionList(drape.controller.jsonController):
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
		now = int(time.time())
		self.setVariable('now', now)

		aParams = self.params()
		uid = drape.util.toInt(aParams.get('uid', -1))
		if uid < 0:
			self.setVariable('errormsg', u'uid参数错误')
			self.setVariable('data', [])
		else:
			self.setVariable('errormsg', '')

			aActionModel = drape.model.LinkedModel('action')

			from_id = drape.util.toInt(aParams.get('from_id', 0))
			if from_id > 0:
				aActionModel.where({
					'ac.id': ('<', from_id)
				})

			actionList = aActionModel.alias('ac').join(
				'userinfo', 'fui', 'ac.from_object_id = fui.id'
			).where(
				from_object_id=uid,
				from_object_type='user'
			).limit(10).order('ac.id DESC').select()

			aTopicModel = drape.model.LinkedModel('discuss_topic')
			aUserinfoModel = drape.model.LinkedModel('userinfo')
			for action in actionList:
				if 'topic' == action['target_object_type']:
					action['target_topic_info'] = aTopicModel.where(
						id=action['target_object_id']
					).find()
				elif 'user' == action['target_object_type']:
					action['target_user_info'] = aUserinfoModel.where(
						id=action['target_object_id']
					).find()
				else:
					raise ValueError('no such target object type: %s' % action['target_object_type'])

			self.setVariable('data', actionList)
