# -*- coding: utf-8 -*-

import frame,app
import drape

class Index(frame.DefaultFrame):
	def process(self):
		self.setTitle(u'首页')
		
		# version
		self.set_variable('testdrape_version',app.version)
		self.set_variable('drape_version',drape.version)
