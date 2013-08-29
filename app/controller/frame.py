# -*- coding: utf-8 -*-

from functools import wraps

import drape
from drape.util import toInt
from drape.model import LinkedModel

import app
from app.lib.cache import Cache


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
		
	def run(self):
		g = self.runbox().variables()
		if 'res' not in g:
			g['res'] = Resource(self)
		
		res = g['res']
		self.set_variable('res',res.create_level(self))
		
		self.set_variable('ROOT', self.request().rootPath())
		self.set_variable('ctrl',self)

		return super(FrameBase, self).run()
		
	def setTitle(self,t):
		g = self.runbox().variables()
		g['title'] = t
		
	def title(self):
		g = self.runbox().variables()
		return g['title']

class DefaultFrame(FrameBase):
	def __init__(self,runbox):
		super(DefaultFrame,self).__init__(runbox)
		self._set_parent('/frame/Layout')

class EmptyFrame(FrameBase):
	def __init__(self,runbox):
		super(EmptyFrame,self).__init__(runbox)
		self._set_parent('/frame/HtmlBody')

class HtmlBody(FrameBase):
	def process(self):
		# res
		g = self.runbox().variables()
		
		reslist = g['res']
		self.set_variable('reslist',reslist)
		
		# title
		sitename = u'testdrape'
		subtitle = u'无标题'
		if 'title' in g:
			subtitle = g['title']
		title = u'%s - %s' % (subtitle, sitename)
		self.set_variable('title', title)
		
		# user id
		aSession = self.session()
		self.set_variable('my_userid', drape.util.toInt(aSession.get('uid', -1)))

		# coffee debug
		if drape.config.get_value('front/coffee_debug'):
			coffee_ext = '.js'
		else:
			coffee_ext = '.min.js'
		self.set_variable('coffee_ext', coffee_ext)

		# version
		self.set_variable('version', app.version)
		self.set_variable('drape_version', drape.version)

class Layout(FrameBase):
	def __init__(self,runbox):
		super(Layout,self).__init__(runbox)
		self._set_parent('/frame/HtmlBody')
		
	def process(self):
		# lib cdn
		self.set_variable('LIBCDN', drape.config.get_value('system/libcdn'))

		# uid
		aSession = self.session()
		uid = aSession.get('uid',-1)
		self.set_variable('uid',uid)
		
		if uid > 0:
			cache = Cache()
			self.set_variable('userinfo', cache.get(
				'userinfo/%s' % uid,
				lambda: LinkedModel('userinfo').where(id=uid).find()
			))
			
			self.set_variable('notice_count', cache.get(
				'notice_count/%s' % uid,
				lambda: LinkedModel('notice').where(
						to_uid = uid,
						isRead = 0,
					).count()
			))
			
			self.set_variable('mail_count', cache.get(
				'mail_count/%s' % uid,
				lambda: LinkedModel('mail').where(
						to_uid = uid,
						isRead = 0
					).count()
			))
			

class NotLogin(DefaultFrame):
	def process(self):
		urlPath = self.request().urlPath()
		self.set_variable('urlPath',urlPath)
		self.set_variable('urlquote',drape.util.urlquote(urlPath))


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
