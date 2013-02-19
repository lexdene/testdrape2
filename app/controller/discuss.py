# -*- coding: utf-8 -*-

import time,os,re

import frame,widget
import drape
import markdown

def emoji(text,imgbasepath):
	reg = re.compile(':([_a-zA-Z0-9]+):')
	text = reg.sub(r'<img class="common_emoji" title=":\1:" alt=":\1:" src="%s/\1.png" align="absmiddle">'%imgbasepath,text)
	return text

class List(frame.DefaultFrame):
	def process(self):
		self.initRes()
		self.setTitle(u'讨论区')
		
		aParams = self.params()
		
		aTopicModel = drape.LinkedModel('discuss_topic')
		
		# pager
		page = drape.util.toInt(aParams.get('page',0))
		count = aTopicModel.count()
		aPager = widget.Pager(total_count=count,current_page=page)
		self.setVariable('page',aPager.run())
		
		aTopicList = aTopicModel \
			.alias('dt') \
			.join('userinfo','topic_ui','dt.uid = topic_ui.id') \
			.join('discuss_topic_cache','tc','tc.id = dt.id') \
			.join('discuss_reply','last_reply','last_reply.id = tc.last_reply_id') \
			.join('userinfo','last_reply_ui','last_reply.uid = last_reply_ui.id') \
			.join('discuss_reply','count_dr','count_dr.tid = dt.id') \
			.field('COUNT(count_dr.id) as reply_count') \
			.order('CASE WHEN last_reply.id is NULL THEN dt.ctime ELSE last_reply.ctime END DESC') \
			.group('dt.id') \
			.reflectField(True) \
			.limit(**aPager.limit()) \
			.select()
		
		self.setVariable('iter',aTopicList)
		self.setVariable('timestr',drape.util.timeStamp2Short)
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		self.setVariable('uid',uid)

class ajaxPostTopic(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = aSession.get('uid',-1)
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','请先登录')
			return
		
		aParams = self.params()
		# validates
		validates = [
			dict(
				key = 'title',
				name = '标题',
				validates = [
					('notempty',),
					('len',4,50)
				]
			) ,
			dict(
				key = 'text',
				name = '内容',
				validates = [
					('notempty',),
					('len',4,500)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		# now
		now = int(time.time())
		
		# insert topic
		aDiscussModel = drape.LinkedModel('discuss_topic')
		topicid = aDiscussModel.insert(dict(
			uid = uid,
			ctime = now,
			title = aParams.get('title',''),
		))
		
		# insert reply
		aReplyModel = drape.LinkedModel('discuss_reply')
		replyid = aReplyModel.insert(dict(
			tid = topicid,
			uid = uid,
			reply_to_id = -1,
			ctime = now,
			text = aParams.get('text','')
		))
		
		# topic cache
		aTopicCacheModel = drape.LinkedModel('discuss_topic_cache')
		aTopicCacheModel.insert(dict(
			id = topicid,
			first_reply_id = replyid,
			last_reply_id = -1
		))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'发表成功')

class Topic(frame.DefaultFrame):
	def process(self):
		self.initRes()
		
		def transText(text):
			if text is None:
				return ''
			text = markdown.markdown(text,safe_mode='escape')
			imgbasepath = self.request().rootPath()+'/static/emoji'
			text = emoji(text,imgbasepath)
			return text
		
		aParams = self.params()
		tid = drape.util.toInt(aParams.get('id',-1))
		if tid < 0:
			self.Error(u'参数无效:缺少id参数或id参数不是整数')
			return
		
		aDiscussModel = drape.LinkedModel('discuss_topic')
		aTopicInfo = aDiscussModel \
			.alias('dt') \
			.join('userinfo','ui','dt.uid = ui.id') \
			.where({'dt.id':tid}) \
			.find()
		
		if aTopicInfo is None:
			self.Error(u'参数无效:没有与id对应的主题')
			return
		
		self.setVariable('topicInfo',aTopicInfo)
		
		aReplyModel = drape.LinkedModel('discuss_reply')
		aReplyIter = aReplyModel \
			.alias('dr') \
			.join('userinfo','ui','dr.uid = ui.id') \
			.join('discuss_reply','rtr','dr.reply_to_id = rtr.id') \
			.join('userinfo','rtrui','rtr.uid = rtrui.id') \
			.where({'dr.tid':tid}) \
			.select()
		for c,reply in enumerate(aReplyIter):
			reply['floor'] = c+1
		
		self.setVariable('aReplyIter',aReplyIter)
		
		self.setVariable('transText',transText)
		self.setVariable('timestr',drape.util.timeStamp2Str)
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		self.setVariable('uid',uid)

class ajaxPostReply(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = aSession.get('uid',-1)
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','请先登录')
			return
		
		aParams = self.params()
		# validates
		validates = [
			dict(
				key = 'tid',
				name = '主题id',
				validates = [
					('int',),
				]
			) ,
			dict(
				key = 'reply_to_id',
				name = '回复id',
				validates = [
					('int',),
				]
			) ,
			dict(
				key = 'text',
				name = '内容',
				validates = [
					('notempty',),
					('len',4,500)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		tid = drape.util.toInt( aParams.get('tid',-1) )
		aReplyModel = drape.LinkedModel('discuss_reply')
		reply_id = aReplyModel.insert(dict(
			tid = tid,
			uid = uid,
			reply_to_id = aParams.get('reply_to_id',-1),
			ctime = int( time.time() ),
			text = aParams.get('text',-1),
		))
		
		aTopicCacheModel = drape.LinkedModel('discuss_topic_cache')
		aTopicCacheModel.where(dict(
			id=tid
		)).update(dict(
			last_reply_id = reply_id
		))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'回复成功')
