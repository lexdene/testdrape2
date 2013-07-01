# -*- coding: utf-8 -*-

import drape

import frame

tables = (
('logininfo',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`loginname` varchar(60) NOT NULL,
	`password` varchar(60) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `loginname` (`loginname`)
'''),
('userinfo',
u'''
	`id` int NOT NULL,
	`nickname` varchar(60) NOT NULL,
	`email` varchar(60) NOT NULL,
	`intro` TEXT NOT NULL,
	`avatar` varchar(100),
	`ctime` int NOT NULL,
	`score` int NOT NULL,
	PRIMARY KEY (`id`)
'''),
('discuss_topic',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`uid` int NOT NULL COMMENT '用户id',
	`ctime` int NOT NULL COMMENT '创建时间',
	`title` varchar(100) NOT NULL COMMENT '标题',
	PRIMARY KEY (`id`)
'''),
('discuss_topic_cache',
u'''
	`id` int NOT NULL,
	`first_reply_id` int NOT NULL,
	`last_reply_id` int NOT NULL,
	PRIMARY KEY(`id`)
'''),
('discuss_reply',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`tid` int NOT NULL COMMENT '主题id',
	`uid` int NOT NULL COMMENT '用户id',
	`reply_to_id` int NOT NULL COMMENT '回复某个回复',
	`ctime` int NOT NULL COMMENT '创建时间',
	`text` TEXT NOT NULL COMMENT '正文',
	PRIMARY KEY (`id`)
'''),
('notice',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`from_uid` int NOT NULL,
	`to_uid` int NOT NULL,
	`item_id` int NOT NULL,
	`type` varchar(20) NOT NULL,
	`ctime` int NOT NULL,
	`isRead` tinyint(1) NOT NULL,
	PRIMARY KEY (`id`)
'''),
('mail',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`from_uid` int NOT NULL,
	`to_uid` int NOT NULL,
	`title` varchar(100) NOT NULL,
	`text` TEXT NOT NULL,
	`ctime` int NOT NULL,
	`isRead` tinyint(1) NOT NULL,
	PRIMARY KEY (`id`)
'''),
('tag',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`content` varchar(100) NOT NULL,
	`ctime` int NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY(`content`)
'''),
('discuss_topic_tag_bridge',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`topic_id` int NOT NULL,
	`tag_id` int NOT NULL,
	PRIMARY KEY (`id`)
'''),
('focus',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`from_uid` int NOT NULL,
	`focus_type` ENUM('user', 'topic', 'tag') NOT NULL,
	`target_id` int NOT NULL,
	`ctime` int NOT NULL,
	`is_del` BOOLEAN NOT NULL,
	PRIMARY KEY (`id`)
'''),

# action表应该是一个巨大的冗余。
# 暂时，设计及实现时仅考虑读取的方便，不考虑冗余问题
('action',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`from_object_id` int NOT NULL,
	`from_object_type` ENUM('user', 'topic', 'tag') NOT NULL,
	`action_type` ENUM('focus', 'post', 'reply') NOT NULL,
	`target_object_id` int NOT NULL,
	`target_object_type` ENUM('user', 'topic', 'tag', 'reply') NOT NULL,
	`ctime` int NOT NULL,
	PRIMARY KEY (`id`)
'''),

('usermsg',
u'''
	`id` int NOT NULL AUTO_INCREMENT,
	`from_uid` int NOT NULL,
	`to_uid` int NOT NULL,
	`text` varchar(200) NOT NULL,
	`ctime` int NOT NULL,
	PRIMARY KEY (`id`)
'''),
)


class DbFrame(frame.DefaultFrame):
	def __init__(self, path):
		super(DbFrame, self).__init__(path)
		self.setParent('/db/Layout')


class Layout(frame.DefaultFrame):
	def process(self):
		self.setTitle(u'数据库')


class CreateTables(DbFrame):
	def process(self):
		aDb = drape.db.Db()
		tablePrefix = aDb.tablePrefix()

		result = []
		for tableName, sql in tables:
			sql = u'CREATE TABLE IF NOT EXISTS `%s%s`(%s)ENGINE=MyISAM DEFAULT CHARSET=utf8' % (
				tablePrefix, tableName, sql
			)
			res = aDb.execute(sql)
			result.append({
				'tableName': tableName,
				'sql': sql,
				'res': res,
				'error': u''
			})

		self.setVariable('result', result)


class DropTables(DbFrame):
	def process(self):
		self.setTemplatePath('/db/CreateTables')
		aDb = drape.application.Application.singleton().db()
		tablePrefix = aDb.tablePrefix()

		result = dict()
		for tableName, sql in tables.iteritems():
			sql = 'drop table if exists `%s%s`' % (tablePrefix, tableName)
			res = aDb.execute(sql)
			result[tableName] = {
				'sql': sql,
				'res': res,
				'error': ''
			}

		self.setVariable('result', result)
