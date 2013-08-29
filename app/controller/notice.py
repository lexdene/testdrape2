# -*- coding: utf-8 -*-

import drape

import frame
from app.lib.cache import remove_cache


class Panel(frame.FrameBase):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		
		aNoticeModel = drape.model.LinkedModel('notice')
		noticeList = aNoticeModel \
			.join('userinfo','fromuser','fromuser.id = notice.from_uid') \
			.where(to_uid=uid,isRead=0).limit(10).select()
		
		aReplyModel = drape.model.LinkedModel('discuss_reply')

		# notice list
		for notice in noticeList:
			if notice['type'] in ('reply_topic', 'reply_to_reply'):
				notice['reply_info'] = aReplyModel.alias('re').join(
					'discuss_topic',
					'dt',
					'dt.id = re.tid'
				).where({'re.id': notice['item_id']}).find()
			elif notice['type'] in ('focus_user', 'usermsg'):
				pass
			else:
				raise ValueError('no such type: %s' % notice['type'])
		
		self.set_variable('noticeList',noticeList)

class setIsRead(drape.controller.JsonController):
	def process(self):
		aSession = self.session()
		uid = drape.util.toInt(aSession.get('uid',-1))
		
		aParams = self.params()
		noticeid = drape.util.toInt(aParams.get('noticeid',-1))
		self.set_variable('noticeid',noticeid)
		
		aNoticeModel = drape.model.LinkedModel('notice')
		noticeInfo = aNoticeModel.where(id=noticeid).find()
		self.set_variable('noticeInfo',noticeInfo)
		if noticeInfo is None:
			self.set_variable('result','failed')
			self.set_variable('msg','no such notice')
			return
		
		if noticeInfo['to_uid'] != uid:
			self.set_variable('result','failed')
			self.set_variable('msg','notice is not for you')
			return
		
		aNoticeModel.where(id=noticeid).update(isRead=1)
		
		self.set_variable('result','success')

		remove_cache('notice_count/%s' % uid)
