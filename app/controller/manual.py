# -*- coding: utf-8 -*-

import frame

class ManualFrame(frame.Markdown):
	def __init__(self,path):
		super(ManualFrame,self).__init__(path)
		self.setParent('/manual/Layout')
		
	def setSubTitle(self,title):
		g = self.globalVars()
		g['subtitle'] = title

class Layout(frame.DefaultFrame):
	def process(self):
		self.initRes()
		
		g = self.globalVars()
		self.setVariable('subtitle',g.get('subtitle'))
		self.setTitle('%s - drape开发手册'%g.get('subtitle'))

class Index(ManualFrame):
	def process(self):
		self.setSubTitle('简介')

class Mvc(ManualFrame):
	def process(self):
		self.setSubTitle('MVC')

class Mvc_Controller(ManualFrame):
	def process(self):
		self.setSubTitle('MVC/Controller')

class Mvc_Model(ManualFrame):
	def process(self):
		self.setSubTitle('MVC/Model')

class Mvc_View(ManualFrame):
	def process(self):
		self.setSubTitle('MVC/View')
