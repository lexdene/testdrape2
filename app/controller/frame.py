# -*- coding: utf-8 -*-

from functools import wraps

import drape
from drape.util import toInt

import app


class Resource(object):
	'''
	管理css / js等资源
	'''
	def __init__(self,controller):
		self.__levels = list()
		self.__resources = list()
		self.__controller = controller

	def __iter__(self):
		for level in reversed(self.__levels):
			for res in level:
				yield res

		for res in self.__resources:
			yield res

	def create_level(self, controller):
		res = Resource(controller)
		self.__levels.append(res)
		return res

	def add(self, path, type=('js', 'css'), version=0):
		if isinstance(type, tuple):
			for i in type:
				self.add(path, i, version)
		else:
			self.__resources.append(dict(
				path = path,
				type = type,
				version = version
			))

	def addResByPath(self, type=('js', 'css'), version=0):
		path = self.__controller.path()
		self.add(path, type, version)

class FrameBase(drape.controller.Controller):
	def notLogin(self):
		self.icRedirect('/frame/NotLogin')
		
	def Error(self, error):
		self.icRedirect(
			'/frame/Error',
			{'error': error}
		)
		
	def postProcess(self):
		g = self.runbox().variables()
		if 'res' not in g:
			g['res'] = Resource(self)
		
		res = g['res']
		self.setVariable('res',res.create_level(self))
		
		self.setVariable('ROOT',self.request().rootPath())
		self.setVariable('ctrl',self)
		
	def setTitle(self,t):
		g = self.runbox().variables()
		g['title'] = t
		
	def title(self):
		g = self.runbox().variables()
		return g['title']

class DefaultFrame(FrameBase):
	def __init__(self,runbox):
		super(DefaultFrame,self).__init__(runbox)
		self.setParent('/frame/Layout')

class EmptyFrame(FrameBase):
	def __init__(self,runbox):
		super(EmptyFrame,self).__init__(runbox)
		self.setParent('/frame/HtmlBody')

class HtmlBody(FrameBase):
	def process(self):
		# res
		g = self.runbox().variables()
		
		reslist = g['res']
		self.setVariable('reslist',reslist)
		
		# title
		sitename = u'testdrape'
		subtitle = u'无标题'
		if 'title' in g:
			subtitle = g['title']
		title = u'%s - %s' % (subtitle, sitename)
		self.setVariable('title', title)
		
		# user id
		aSession = self.session()
		self.setVariable('my_userid', drape.util.toInt(aSession.get('uid', -1)))

		# coffee debug
		if drape.config.get_value('front/coffee_debug'):
			coffee_ext = '.js'
		else:
			coffee_ext = '.min.js'
		self.setVariable('coffee_ext', coffee_ext)

		# version
		self.setVariable('version', app.version)
		self.setVariable('drape_version', drape.version)

class Layout(FrameBase):
	def __init__(self,runbox):
		super(Layout,self).__init__(runbox)
		self.setParent('/frame/HtmlBody')
		
	def process(self):
		# lib cdn
		self.setVariable('LIBCDN', drape.config.get_value('system/libcdn'))

		# uid
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


@DefaultFrame.controller
def Error(self):
	pass


def check_login(fun):
	''' 判断是否登录
	    未登录，则显示NotLogin
	'''
	@wraps(fun)
	def new_fun(self):
		fun(self)

		session = self.session()
		uid = toInt(session.get('uid', -1))
		if uid < 0:
			self.notLogin()

	return new_fun
