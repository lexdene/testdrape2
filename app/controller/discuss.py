# -*- coding: utf-8 -*-

import time

import drape

import frame
import userinfo
import app.lib.text
from app.lib.tags import Tags
from app.model.discuss import TopicModel

DEFAULT_CLS = 'List'

class List(frame.DefaultFrame):
	def process(self):
		aParams = self.params()
		
		# tag id
		tagid = aParams.get('tag',None)

		# tag info
		if tagid > 0:
			tag_model = drape.model.LinkedModel('tag')
			tag_info = tag_model.where(id=tagid).find()

			ttb_model = drape.model.LinkedModel('discuss_topic_tag_bridge')
			tag_info['topic_count'] = ttb_model.where(tag_id=tagid).count()
			self.setVariable('tag_info', tag_info)
			self.setTitle(u'标签: %s' % tag_info['content'])
		else:
			self.setVariable('tag_info', None)
			self.setTitle(u'讨论区')

		aTopicModel = TopicModel()
		
		# pager
		page = drape.util.toInt(aParams.get('page',0))
		count = aTopicModel.getTopicCount(tagid=tagid)
		aPager = self.runbox().controller('/widget/Pager',total_count=count,current_page=page)
		self.setVariable('page',aPager)
		
		self.setVariable('topic_list',aTopicModel.getTopicList(tagid=tagid, **aPager.limit()) )
		self.setVariable('timestr',app.lib.text.timeStamp2Short)
		self.setVariable('avatar',userinfo.avatarFunc(self.request().rootPath()) )
		
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
				name = u'标题',
				validates = [
					('notempty',),
					('len',4,50)
				]
			) ,
			dict(
				key = 'text',
				name = u'内容',
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
		
		# tags
		tags = Tags()
		tags.setTagString( aParams.get('tags','') )

		# validate tags
		res = tags.validate()
		if False == res['result']:
			self.setVariable('result', 'failed')
			self.setVariable('msg', res['msg'])
			return

		# get tag id list
		tagIdList = tags.idListInDb()

		# now
		now = int(time.time())
		
		# insert topic
		aDiscussModel = drape.model.LinkedModel('discuss_topic')
		topicid = aDiscussModel.insert(
			uid = uid,
			ctime = now,
			title = aParams.get('title',''),
		)
		
		# insert reply
		aReplyModel = drape.model.LinkedModel('discuss_reply')
		replyid = aReplyModel.insert(
			tid = topicid,
			uid = uid,
			reply_to_id = -1,
			ctime = now,
			text = aParams.get('text','')
		)
		
		# topic cache
		aTopicCacheModel = drape.model.LinkedModel('discuss_topic_cache')
		aTopicCacheModel.insert(
			id = topicid,
			first_reply_id = replyid,
			last_reply_id = replyid
		)

		# topic tag bridge
		aBridgeModel = drape.model.LinkedModel('discuss_topic_tag_bridge')
		aBridgeModel.insert(
			tag_id = tagIdList,
			topic_id = [topicid] * len( tagIdList )
		)

		# action
		# user post topic
		aActionModel = drape.model.LinkedModel('action')
		aActionModel.insert(
			from_object_id=uid,
			from_object_type='user',
			action_type='post',
			target_object_id=topicid,
			target_object_type='topic',
			ctime=now
		)

		# tag post topic
		aActionModel.insert(
			from_object_id=tagIdList,
			from_object_type='tag',
			action_type='post',
			target_object_id=topicid,
			target_object_type='topic',
			ctime=now
		)

		self.setVariable('result','success')
		self.setVariable('msg',u'发表成功')

class Topic(frame.DefaultFrame):
	def process(self):
		aParams = self.params()
		tid = drape.util.toInt(aParams.get('id',-1))
		if tid < 0:
			self.Error(u'参数无效:缺少id参数或id参数不是整数')
			return
		
		aDiscussModel = drape.model.LinkedModel('discuss_topic')
		aTopicInfo = aDiscussModel \
			.alias('dt') \
			.join('userinfo','ui','dt.uid = ui.id') \
			.where({'dt.id':tid}) \
			.find()
		
		if aTopicInfo is None:
			self.Error(u'参数无效:没有与id对应的主题')
			return
		
		self.setVariable('topicInfo',aTopicInfo)
		self.setTitle(u'%s - 讨论区'%aTopicInfo['title'])

		aReplyModel = drape.model.LinkedModel('discuss_reply')
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
		
		aTagModel = drape.model.LinkedModel('tag')
		aTagIter = aTagModel \
			.join('discuss_topic_tag_bridge','ttb','ttb.tag_id = tag.id') \
			.where({'ttb.topic_id':tid}) \
			.select()
		
		self.setVariable('aTagIter',aTagIter)
		
		self.setVariable('timestr',app.lib.text.timeStamp2Str)
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
		aReplyModel = drape.model.LinkedModel('discuss_reply')
		reply_id = aReplyModel.insert(
			tid = tid,
			uid = uid,
			reply_to_id = reply_to_id,
			ctime = now,
			text = aParams.get('text',''),
		)
		
		# topic cache table
		aTopicCacheModel = drape.model.LinkedModel('discuss_topic_cache')
		aTopicCacheModel.where(id=tid).update(last_reply_id = reply_id)
		
		# models
		aTopicModel = drape.model.LinkedModel('discuss_topic')
		aNoticeModel = drape.model.LinkedModel('notice')
		aNoticeCacheModel = drape.model.LinkedModel('notice_cache')
		
		# topic info
		topicInfo = aTopicModel.where(id=tid).find()
		
		# reply info
		replyToReplyInfo = aReplyModel.where(id=reply_to_id).find()
		
		# reply topic notice
		# except to myself
		if uid != topicInfo['uid'] \
			and (not replyToReplyInfo or replyToReplyInfo['uid'] != topicInfo['uid']):
			noticeId = aNoticeModel.insert(
				from_uid = uid,
				to_uid = topicInfo['uid'],
				item_id = reply_id,
				type = 'reply_topic',
				ctime = now,
				isRead = False,
			)
		
		# reply to reply notice
		# except to myself
		if replyToReplyInfo and uid != replyToReplyInfo['uid']:
			noticeId = aNoticeModel.insert(
				from_uid = uid,
				to_uid = replyToReplyInfo['uid'],
				item_id = reply_id,
				type = 'reply_to_reply',
				ctime = now,
				isRead = False,
			)
		
		# action
		# user reply topic
		aActionModel = drape.model.LinkedModel('action')
		aActionModel.insert(
			from_object_id=uid,
			from_object_type='user',
			action_type='reply',
			target_object_id=reply_id,
			target_object_type='reply',
			ctime=now
		)

		# topic has reply
		aActionModel.insert(
			from_object_id=tid,
			from_object_type='topic',
			action_type='reply',
			target_object_id=reply_id,
			target_object_type='reply',
			ctime=now
		)

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
				name = u'内容',
				validates = [
					('notempty',),
					('len',4,25000)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		reply_id = drape.util.toInt(aParams.get('reply_id'),-1)
		aReplyModel = drape.model.LinkedModel('discuss_reply')
		replyinfo = aReplyModel.where(id=reply_id).find()
		if replyinfo is None or uid != replyinfo['uid']:
			self.setVariable('result','failed')
			self.setVariable('msg','您无权修改此回复')
			return
		
		aReplyModel.where(id=reply_id).update(text=aParams.get('text',''))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'修改成功')
