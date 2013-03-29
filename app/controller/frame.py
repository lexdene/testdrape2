# -*- coding: utf-8 -*-

import drape
import app

class FrameBase(drape.controller.Controller):
	def notLogin(self):
		self.icRedirect('/frame/NotLogin')
		
	def Error(self,error):
		self.icRedirect('/frame/Error',error)
		
	def postProcess(self):
		g = self.globalVars()
		if 'res' not in g:
			g['res'] = list()
		
		myres = list()
		g['res'].append(myres)
		self.setVariable('res',myres)
		
		self.setVariable('ROOT',self.request().rootPath())
		self.setVariable('ctrl',self)
		
	def setTitle(self,t):
		g = self.globalVars()
		g['title'] = t
		
	def title(self):
		g = self.globalVars()
		return g['title']
		
	def addResByPath(self,type='both',path=None):
		# path
		if path is None:
			path = self.path()
		
		res = self.variable('res')
		
		if type in ['both','css']:
			res.append(('css%s'%path,'css'))
		if type in ['both','js']:
			res.append(('js%s'%path,'js'))

class DefaultFrame(FrameBase):
	def __init__(self,path):
		super(DefaultFrame,self).__init__(path)
		self.setParent('/frame/Layout')

class EmptyFrame(FrameBase):
	def __init__(self,path):
		super(EmptyFrame,self).__init__(path)
		self.setParent('/frame/HtmlBody')

class HtmlBody(FrameBase):
	def process(self):
		# res
		g = self.globalVars()
		
		reslist = g['res'][::-1]
		self.setVariable('reslist',reslist)
		
		# title
		sitename = u'testdrape'
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

class Layout(FrameBase):
	def __init__(self,path):
		super(Layout,self).__init__(path)
		self.setParent('/frame/HtmlBody')
		
	def process(self):
		aSession = self.session()
		uid = aSession.get('uid',-1)
		self.setVariable('uid',uid)
		
		if uid > 0:
			aUserinfoModel = drape.model.LinkedModel('userinfo')
			userinfo = aUserinfoModel.where(id=uid).find()
			self.setVariable('userinfo',userinfo)
			
			aNoticeModel = drape.model.LinkedModel('notice')
			noticeCount = aNoticeModel.where(
				to_uid = uid,
				isRead = 0,
			).count()
			self.setVariable('notice_count',noticeCount)
			
			aMailModel = drape.model.LinkedModel('mail')
			mailCount = aMailModel.where(
				to_uid = uid,
				isRead = 0
			).count()
			self.setVariable('mail_count',mailCount)

class NotLogin(DefaultFrame):
	def process(self):
		urlPath = self.request().urlPath()
		self.setVariable('urlPath',urlPath)
		self.setVariable('urlquote',drape.util.urlquote(urlPath))

class Error(DefaultFrame):
	def process(self):
		self.setVariable('error',self.ctrlParams()[0])
