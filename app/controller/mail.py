# -*- coding: utf-8 -*-

import datetime

import drape

from . import frame
from app.lib.text import datetime2Str
from app.lib.cache import remove_cache

class Write(frame.DefaultFrame):
	def process(self):
		self.setTitle('发送私信')
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()
		
		aParams = self.params()
		to_uid = drape.util.toInt(aParams.get('to_uid',-1))
		
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		to_userinfo = aUserinfoModel.where(id=to_uid).find()
		if to_userinfo is None:
			self.Error('用户不存在: %s' % to_uid)
		
		self.set_variable('to_userinfo',to_userinfo)

class ajaxWrite(drape.controller.JsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.set_variable('result','failed')
			self.set_variable('msg','请先登录')
			return
		
		aParams = self.params()
		# validates
		validates = [
			dict(
				key = 'to_uid',
				name = '收件人id',
				validates = [
					('notempty',),
					('int',)
				]
			) ,
			dict(
				key = 'title',
				name = '标题',
				validates = [
					('notempty',),
					('len',4,50)
				]
			) ,
			dict(
				key = 'text',
				name = '内容',
				validates = [
					('notempty',),
					('len',4,2000)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.set_variable('result','failed')
			self.set_variable('msg',res['msg'])
			return
		
		aMailModel = drape.model.LinkedModel('mail')
		data = dict(aParams)
		data['from_uid'] = uid
		data['ctime'] = datetime.datetime.now()
		data['isRead'] = 0
		aMailModel.insert(**data)

		# clean up cache
		remove_cache('mail_count/%s' % aParams['to_uid'])
		
		self.set_variable('result','success')

class MailBox(frame.FrameBase):
	def __init__(self,path):
		super(MailBox,self).__init__(path)
		self._set_parent('mail/MailBoxLayout')

class MailBoxLayout(frame.DefaultFrame):
	def process(self):
		g = self.runbox().variables()
		self.set_variable('title',g.get('title'))

class ReceiveBox(MailBox):
	def process(self):
		self.setTitle('收件箱')
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()
		
		aMailModel = drape.model.LinkedModel('mail')
		maillist = aMailModel \
			.join('userinfo','fromuser','fromuser.id=mail.from_uid') \
			.where(to_uid = uid).select()
		
		self.set_variable('maillist',maillist)
		self.set_variable('timestr', datetime2Str)
