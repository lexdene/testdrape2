# -*- coding: utf-8 -*-

import time
import drape
import frame,app.lib.text

class Write(frame.DefaultFrame):
	def process(self):
		self.initRes()
		self.setTitle('发送私信')
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()
		
		aParams = self.params()
		to_uid = drape.util.toInt(aParams.get('to_uid',-1))
		
		aUserinfoModel = drape.LinkedModel('userinfo')
		to_userinfo = aUserinfoModel.where(id=to_uid).find()
		if to_userinfo is None:
			self.Error('用户不存在')
		
		self.setVariable('to_userinfo',to_userinfo)

class ajaxWrite(drape.jsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','请先登录')
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
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		aMailModel = drape.LinkedModel('mail')
		data = dict(aParams)
		data['from_uid'] = uid
		data['ctime'] = int(time.time())
		data['isRead'] = 0
		aMailModel.insert(**data)
		
		self.setVariable('result','success')

class MailBox(frame.FrameBase):
	def __init__(self,path):
		super(MailBox,self).__init__(path)
		self.setParent('/mail/MailBoxLayout')

class MailBoxLayout(frame.DefaultFrame):
	def process(self):
		self.initRes()
		
		g = self.globalVars()
		self.setVariable('title',g.get('title'))

class ReceiveBox(MailBox):
	def process(self):
		self.initRes()
		self.setTitle('收件箱')
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()
		
		aMailModel = drape.LinkedModel('mail')
		maillist = aMailModel \
			.join('userinfo','fromuser','fromuser.id=mail.from_uid') \
			.where(to_uid = uid).select()
		
		self.setVariable('maillist',maillist)
		self.setVariable('transText',app.lib.text.transText)
		self.setVariable('timestr',drape.util.timeStamp2Str)
