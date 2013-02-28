# -*- coding: utf-8 -*-

import os,hashlib
import drape
import frame

class UploadImage(frame.EmptyFrame):
	def process(self):
		aParams = self.params()
		accept = aParams.get('accept','')
		self.setVariable('accept',accept)

class UploadImageResult(frame.EmptyFrame):
	def process(self):
		aParams = self.params()
		accept = aParams.get('accept','')
		self.setVariable('accept',accept)
		
		def checkFileType(fileType,acceptType):
			if '' == acceptType:
				return True
			l = acceptType.split(',')
			if fileType in l:
				return True
			else:
				return False
		
		key = 'file'
		aFiles = self.files()
		
		if key in aFiles:
			myfile = aFiles[key]
			
			import drape.debug
			drape.debug.debug(myfile.type)
			if not checkFileType(myfile.type,accept):
				self.setVariable('result','文件类型错误')
				return
			
			sufix = os.path.splitext(myfile.filename)[1][1:]
			
			m = hashlib.sha1()
			m.update(myfile.file.read())
			saveFileName = m.hexdigest()
			
			filepath = '%s.%s'%(saveFileName,sufix)
			
			savepath = self.saveUploadFile(myfile,filepath)
			self.setVariable('savepath',savepath)
			self.setVariable('result','success')
		else:
			self.setVariable('result','未上传文件')
