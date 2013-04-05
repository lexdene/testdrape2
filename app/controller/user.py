# -*- coding: utf-8 -*-

import time

import frame,userinfo
import drape

import validatecode

common_validates = dict(
	password = dict(
		key = 'password',
		name = '密码',
		validates = [
			('notempty',),
			('len',4,20)
		]
	) ,
	repassword = dict(
		key = 'repassword',
		name = '重复密码',
		validates = [
			('notempty',),
			('equal','password','密码')
		]
	) ,
)

def encrypt_password(original):
	s = '%s|%s'%(
		'original',
		drape.util.md5sum('drape')
	)
	return drape.util.md5sum(s)

class Login(frame.DefaultFrame):
	def process(self):
		self.setTitle(u'登录')
		
		aParams = self.params()
		redirect = aParams.get('redirect','/')
		self.setVariable('redirect',redirect)

class ajaxLogin(drape.controller.jsonController):
	def process(self):
		aParams = self.params()
		
		if not validatecode.validate(
			self.params().get('valcode'),
			self.session()
		):
			self.setVariable('result','failed')
			self.setVariable('msg',u'验证码错误')
			return
		
		# validates
		validates = [
			dict(
				key = 'loginname',
				name = '登录名',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'password',
				name = '密码',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		aLoginModel = drape.model.LinkedModel('logininfo')
		res = aLoginModel.where(loginname=aParams['loginname']).find()
		
		if res is None:
			self.setVariable('result','failed')
			self.setVariable('msg',u'登录名不存在')
			return
		elif res['password'] != encrypt_password(aParams['password']):
			self.setVariable('result','failed')
			self.setVariable('msg',u'密码错误')
			return
		else:
			self.setVariable('result','success')
			
			aSession = self.session()
			aSession.set('uid',res['id'])

class Register(frame.DefaultFrame):
	def process(self):
		self.setTitle(u'注册')
		
		aParams = self.params()
		redirect = aParams.get('redirect','/')
		self.setVariable('redirect',redirect)

class ajaxRegister(drape.controller.jsonController):
	def process(self):
		aParams = self.params()
		
		if not validatecode.validate(
			self.params().get('valcode'),
			self.session()
		):
			self.setVariable('result','failed')
			self.setVariable('msg',u'验证码错误')
			return
		
		# validates
		validates = [
			dict(
				key = 'loginname',
				name = u'登录名',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'password',
				name = u'密码',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'repassword',
				name = u'重复密码',
				validates = [
					('notempty',),
					('equal','password','密码')
				]
			) ,
			dict(
				key = 'nickname',
				name = u'昵称',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'email',
				name = u'电子邮箱',
				validates = [
					('notempty',),
					('email',)
				]
			) ,
			dict(
				key = 'intro',
				name = u'个人介绍',
				validates = [
					('notempty',),
					('len',4,1000)
				]
			) ,
		]
		
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		aLogininfoModel = drape.model.LinkedModel('logininfo')
		res = aLogininfoModel.where(loginname=aParams.get('loginname')).select()
		if len(res) > 0:
			self.setVariable('result','failed')
			self.setVariable('msg','存在登录名相同的用户，无法注册')
			return
		
		id = aLogininfoModel.insert(
			loginname = aParams.get('loginname'),
			password = encrypt_password(aParams.get('password'))
		)
		self.setVariable('id',id)
		
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		aUserinfoModel.insert(
			id = id,
			nickname = aParams.get('nickname'),
			email = aParams.get('email'),
			intro = aParams.get('intro'),
			ctime = time.time(),
			score = 0,
		)
		
		self.setVariable('result','success')

class Logout(frame.DefaultFrame):
	def process(self):
		self.setTitle(u'退出登录')
		
		aSession = self.session()
		aSession.remove('uid')
		
		aParams = self.params()
		redirect = aParams.get('redirect','/')
		self.setVariable('redirect',redirect)

class UserCenterFrame(frame.FrameBase):
	def __init__(self,path):
		super(UserCenterFrame,self).__init__(path)
		self.setParent('/user/UserCenterLayout')

class UserCenterLayout(frame.DefaultFrame):
	def process(self):
		self.setVariable('title',self.title())

class UserCenter(UserCenterFrame):
	def process(self):
		self.setTitle(u'个人中心')
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()

class EditUserInfo(UserCenterFrame):
	def process(self):
		self.setTitle(u'修改个人资料')
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()
		
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		aUserinfo = aUserinfoModel.where(id=uid).find()
		
		self.setVariable('userinfo',aUserinfo)
		self.setVariable('avatar',userinfo.avatarFunc(self.request().rootPath()) )

class ajaxEditUserInfo(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','未登录用户不能修改用户资料')
			return
		
		aParams = self.params()
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		aUserinfoModel.where(id=uid).update(**aParams)
		
		self.setVariable('result','success')
		self.setVariable('msg',u'修改成功')

class ChangePassword(UserCenterFrame):
	def process(self):
		self.setTitle(u'修改密码')
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.notLogin()

class ajaxChangePassword(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','未登录用户不能修改用户资料')
			return
		
		aParams = self.params()
		aLogininfoModel = drape.model.LinkedModel('logininfo')
		logininfo = aLogininfoModel.where(uid=uid).find()
		
		# oldpassword
		oldpassword = aParams.get('oldpassword','')
		newpassword = aParams.get('password','')
		renewpassword = aParams.get('repassword','')
		if encrypt_password(oldpassword) != logininfo['password']:
			self.setVariable('result','failed')
			self.setVariable('msg','原密码不正确')
			return
		
		validates = [
			common_validates['password'],
			common_validates['repassword']
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		aLogininfoModel.where(uid=uid).update(password = encrypt_password(newpassword))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'修改成功')
