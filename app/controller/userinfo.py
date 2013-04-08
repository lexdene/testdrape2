# -*- coding: utf-8 -*-

import drape

import frame
import app.lib.text

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
		self.setVariable('userinfo',userinfo)
		self.setVariable('timestr',app.lib.text.timeStamp2Str)
		self.setVariable('avatar',avatarFunc(self.request().rootPath()) )

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
