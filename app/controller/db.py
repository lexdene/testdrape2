# -*- coding: utf-8 -*-

import drape
import frame

tables = {
'logininfo' :
'''CREATE TABLE IF NOT EXISTS `%slogininfo` (
	`id` int NOT NULL AUTO_INCREMENT,
	`loginname` varchar(60) NOT NULL,
	`password` varchar(60) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `loginname` (`loginname`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'userinfo' :
'''CREATE TABLE IF NOT EXISTS `%suserinfo` (
	`id` int NOT NULL,
	`nickname` varchar(60) NOT NULL,
	`email` varchar(60) NOT NULL,
	`intro` TEXT NOT NULL,
	`avatar` varchar(100),
	`ctime` int NOT NULL,
	`score` int NOT NULL,
	PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'discuss_topic' :
'''CREATE TABLE IF NOT EXISTS `%sdiscuss_topic`(
	`id` int NOT NULL AUTO_INCREMENT,
	`uid` int NOT NULL COMMENT '用户id',
	`ctime` int NOT NULL COMMENT '创建时间',
	`title` varchar(100) NOT NULL COMMENT '标题',
	PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'discuss_topic_cache':
'''CREATE TABLE IF NOT EXISTS `%sdiscuss_topic_cache`(
	`id` int NOT NULL,
	`first_reply_id` int NOT NULL,
	`last_reply_id` int NOT NULL,
	PRIMARY KEY(`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'discuss_reply' :
'''CREATE TABLE IF NOT EXISTS `%sdiscuss_reply`(
	`id` int NOT NULL AUTO_INCREMENT,
	`tid` int NOT NULL COMMENT '主题id',
	`uid` int NOT NULL COMMENT '用户id',
	`reply_to_id` int NOT NULL COMMENT '回复某个回复',
	`ctime` int NOT NULL COMMENT '创建时间',
	`text` TEXT NOT NULL COMMENT '正文',
	PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'notice' :
'''CREATE TABLE IF NOT EXISTS `%snotice`(
	`id` int NOT NULL AUTO_INCREMENT,
	`from_uid` int NOT NULL,
	`to_uid` int NOT NULL,
	`item_id` int NOT NULL,
	`type` varchar(20) NOT NULL,
	`ctime` int NOT NULL,
	`isRead` tinyint(1) NOT NULL,
	PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'notice_cache' :
'''CREATE TABLE IF NOT EXISTS `%snotice_cache`(
	`id` int NOT NULL AUTO_INCREMENT,
	`data` TEXT NOT NULL,
	PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
'mail' :
'''CREATE TABLE IF NOT EXISTS `%smail`(
	`id` int NOT NULL AUTO_INCREMENT,
	`from_uid` int NOT NULL,
	`to_uid` int NOT NULL,
	`title` varchar(100) NOT NULL,
	`text` TEXT NOT NULL,
	`ctime` int NOT NULL,
	`isRead` tinyint(1) NOT NULL,
	PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
}

class DbFrame(frame.DefaultFrame):
	def __init__(self,path):
		super(DbFrame,self).__init__(path)
		self.setParent('/db/Layout')

class Layout(frame.DefaultFrame):
	def process(self):
		self.setTitle('数据库')

class CreateTables(DbFrame):
	def process(self):
		aDb = drape.application.Application.singleton().db()
		tablePrefix = aDb.tablePrefix()
		
		result = dict()
		for tableName,sql in tables.iteritems():
			sql = sql%tablePrefix
			res = aDb.execute(sql)
			result[tableName] = {
				'sql' : sql,
				'res' : res ,
				'error' : ''
			}
		
		self.setVariable('result',result)

class DropTables(DbFrame):
	def process(self):
		self.setTemplatePath('/db/CreateTables')
		aDb = drape.application.Application.singleton().db()
		tablePrefix = aDb.tablePrefix()
		
		result = dict()
		for tableName,sql in tables.iteritems():
			sql = 'drop table if exists `%s%s`'%(tablePrefix,tableName)
			res = aDb.execute(sql)
			result[tableName] = {
				'sql' : sql,
				'res' : res ,
				'error' : ''
			}
		
		self.setVariable('result',result)
