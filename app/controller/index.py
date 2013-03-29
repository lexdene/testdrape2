# -*- coding: utf-8 -*-

import frame,app
import drape

class Index(frame.DefaultFrame):
	def process(self):
		self.setTitle(u'首页')
		
		# version
		self.setVariable('testdrape_version',app.version)
		self.setVariable('drape_version',drape.version)
