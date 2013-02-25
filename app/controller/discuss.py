# -*- coding: utf-8 -*-

import time,os,re,json

import frame,widget,userinfo,app.lib.emoji
import drape
import markdown

def emoji(text,imgbasepath):
	reg = re.compile(':([_a-zA-Z0-9]+):')
	def filter_emoji(matchObj):
		match_string = matchObj.group(0)
		emoji_string = match_string[1:-1]
		if app.lib.emoji.isEmoji(emoji_string):
			return r'<img class="common_emoji" title="%(emoji)s" alt="%(emoji)s" src="%(basepath)s/%(emoji)s.png" align="absmiddle">'%dict(
				basepath = imgbasepath,
				emoji = emoji_string
			)
		else:
			return match_string
		
	text = reg.sub(filter_emoji,text)
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
		uid = drape.util.toInt(aSession.get('uid',-1))
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
			imgbasepath = 'https://a248.e.akamai.net/assets.github.com/images/icons/emoji'
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
		self.setVariable('avatar',userinfo.avatarFunc(self.request().rootPath()) )
		
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		self.setVariable('uid',uid)

class ajaxPostReply(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
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
		reply_to_id = drape.util.toInt( aParams.get('reply_to_id',-1) )
		now = int( time.time() )
		
		# reply table
		aReplyModel = drape.LinkedModel('discuss_reply')
		reply_id = aReplyModel.insert(dict(
			tid = tid,
			uid = uid,
			reply_to_id = reply_to_id,
			ctime = now,
			text = aParams.get('text',''),
		))
		
		# topic cache table
		aTopicCacheModel = drape.LinkedModel('discuss_topic_cache')
		aTopicCacheModel.where(dict(
			id=tid
		)).update(dict(
			last_reply_id = reply_id
		))
		
		# notice
		
		# models
		aTopicModel = drape.LinkedModel('discuss_topic')
		aNoticeModel = drape.LinkedModel('notice')
		aNoticeCacheModel = drape.LinkedModel('notice_cache')
		
		# topic info
		topicInfo = aTopicModel.where(dict(id=tid)).find()
		
		# reply topic notice
		# except to myself
		if uid != topicInfo['uid']:
			noticeId = aNoticeModel.insert(dict(
				from_uid = uid,
				to_uid = topicInfo['uid'],
				item_id = tid,
				type = 'reply_topic',
				ctime = now,
				isRead = False,
			))
			
			aNoticeCacheModel.insert(dict(
				id = noticeId,
				data = json.dumps(dict(
					topic_title = topicInfo['title'],
				))
			))
		
		# reply to reply notice
		# except to myself
		replyToReplyInfo = aReplyModel.where(dict(id=reply_to_id)).find()
		if replyToReplyInfo and uid != replyToReplyInfo['uid']:
			noticeId = aNoticeModel.insert(dict(
				from_uid = uid,
				to_uid = replyToReplyInfo['uid'],
				item_id = reply_to_id,
				type = 'reply_to_reply',
				ctime = now,
				isRead = False,
			))
			
			aNoticeCacheModel.insert(dict(
				id = noticeId,
				data = json.dumps(dict(
					topic_title = topicInfo['title'],
				))
			))
		
		# success
		self.setVariable('result','success')
		self.setVariable('msg',u'回复成功')

class ajaxEditReply(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','请先登录')
			return
		
		aParams = self.params()
		# validates
		validates = [
			dict(
				key = 'reply_id',
				name = 'reply id',
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
		
		reply_id = drape.util.toInt(aParams.get('reply_id'),-1)
		aReplyModel = drape.LinkedModel('discuss_reply')
		replyinfo = aReplyModel.where(dict(id=reply_id)).find()
		if replyinfo is None or uid != replyinfo['uid']:
			self.setVariable('result','failed')
			self.setVariable('msg','您无权修改此回复')
			return
		
		aReplyModel.where(dict(id=reply_id)).update(dict(text=aParams.get('text','')))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'修改成功')
