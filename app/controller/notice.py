# -*- coding: utf-8 -*-

import json

import drape

import frame

class Panel(frame.FrameBase):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		
		aNoticeModel = drape.model.LinkedModel('notice')
		noticeList = aNoticeModel \
			.join('userinfo','fromuser','fromuser.id = notice.from_uid') \
			.join('notice_cache','cache','cache.id = notice.id') \
			.where(to_uid=uid,isRead=0).select()
		
		for notice in noticeList:
			notice['cache.data'] = json.loads(notice['cache.data'])
		
		self.setVariable('noticeList',noticeList)

class setIsRead(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		
		aParams = self.params()
		noticeid = drape.util.toInt(aParams.get('noticeid',-1))
		self.setVariable('noticeid',noticeid)
		
		aNoticeModel = drape.model.LinkedModel('notice')
		noticeInfo = aNoticeModel.where(id=noticeid).find()
		self.setVariable('noticeInfo',noticeInfo)
		if noticeInfo is None:
			self.setVariable('result','failed')
			self.setVariable('msg','no such notice')
			return
		
		if noticeInfo['to_uid'] != uid:
			self.setVariable('result','failed')
			self.setVariable('msg','notice is not for you')
			return
		
		aNoticeModel.where(id=noticeid).update(isRead=1)
		
		self.setVariable('result','success')
