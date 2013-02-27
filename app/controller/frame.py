# -*- coding: utf-8 -*-

import drape
import app

class FrameBase(drape.NestingController):
	def notLogin(self):
		self.icRedirect('/frame/NotLogin')
		
	def Error(self,error):
		self.icRedirect('/frame/Error',error)

class DefaultFrame(FrameBase):
	def __init__(self,path):
		super(DefaultFrame,self).__init__(path)
		self.setParent('/frame/Layout')

class EmptyFrame(FrameBase):
	def __init__(self,path):
		super(EmptyFrame,self).__init__(path)
		self.setParent('/frame/HtmlBody')

class HtmlBody(drape.NestingController):
	def beforeChildProcess(self):
		g = self.globalVars()
		g.clear()
		g['res'] = list()
		
	def process(self):
		# res
		g = self.globalVars()
		
		reslist = g['res'][::-1]
		self.setVariable('reslist',reslist)
		
		# title
		sitename = u'JDMD Online Judge'
		subtitle = u'无标题'
		if 'title' in g:
			subtitle = g['title']
		title = '%s - %s'%(subtitle,sitename)
		self.setVariable('title',title)
		
		# version
		self.setVariable('version',app.version)
		self.setVariable('drape_version',drape.version)
		
		# user id
		self.setVariable('my_userid',-1)

class Layout(drape.NestingController):
	def __init__(self,path):
		super(Layout,self).__init__(path)
		self.setParent('/frame/HtmlBody')
		
	def process(self):
		self.initRes()
		
		aSession = self.session()
		uid = aSession.get('uid',-1)
		self.setVariable('uid',uid)
		
		if uid > 0:
			aUserinfoModel = drape.LinkedModel('userinfo')
			userinfo = aUserinfoModel.where(id=uid).find()
			self.setVariable('userinfo',userinfo)
			
			aNoticeModel = drape.LinkedModel('notice')
			noticeCount = aNoticeModel.where(
				to_uid = uid,
				isRead = 0,
			).count()
			self.setVariable('notice_count',noticeCount)
			
			aMailModel = drape.LinkedModel('mail')
			mailCount = aMailModel.where(
				to_uid = uid,
				isRead = 0
			).count()
			self.setVariable('mail_count',mailCount)
		
		self.setVariable('testdrape_version',app.version)
		self.setVariable('drape_version',drape.version)

class NotLogin(DefaultFrame):
	def process(self):
		self.initRes()
		urlPath = self.request().urlPath()
		self.setVariable('urlPath',urlPath)
		self.setVariable('urlquote',drape.util.urlquote(urlPath))

class Error(DefaultFrame):
	def process(self):
		self.setVariable('error',self.ctrlParams()[0])
