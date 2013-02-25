# -*- coding: utf-8 -*-

import json

import drape

class Panel(drape.ViewController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		
		aNoticeModel = drape.LinkedModel('notice')
		noticeList = aNoticeModel \
			.join('userinfo','fromuser','fromuser.id = notice.from_uid') \
			.join('notice_cache','cache','cache.id = notice.id') \
			.where(dict(to_uid=uid)).select()
		
		for notice in noticeList:
			notice['cache.data'] = json.loads(notice['cache.data'])
		
		self.setVariable('noticeList',noticeList)
