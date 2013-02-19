# -*- coding: utf-8 -*-

import frame
import drape

class MainPage(frame.DefaultFrame):
	def process(self):
		aParams = self.params()
		uid = drape.util.toInt(aParams.get('id',-1))
		if uid < 0:
			self.Error(u'参数无效:id格式非法')
			return
		
		aUserinfoModel = drape.LinkedModel('userinfo')
		userinfo = aUserinfoModel.where(dict(id=uid)).find()
		if userinfo is None:
			self.Error(u'无此用户')
			return
		
		self.initRes()
		self.setTitle(userinfo['nickname'])
		self.setVariable('userinfo',userinfo)
		self.setVariable('timestr',drape.util.timeStamp2Str)
