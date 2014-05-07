# -*- coding: utf-8 -*-
''' create tables in db '''
from drape.db import Db
from drape.response import json_response

__tables__ = (
    ("logininfo", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `loginname` VARCHAR(60) NOT NULL,\n"
        "    `password` VARCHAR(60) NOT NULL,\n"
        "    PRIMARY KEY(`id`),\n"
        "    UNIQUE KEY (`loginname`)\n"
        )
     ),
    ("userinfo", (
        "    `id` INT NOT NULL,\n"
        "    `nickname` VARCHAR(60) NOT NULL,\n"
        "    `email` VARCHAR(60) NOT NULL,\n"
        "    `intro` TEXT NOT NULL,\n"
        "    `avatar` VARCHAR(100),\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    `score` INT NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("discuss_topic", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `uid` INT NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    `title` VARCHAR(100) NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("discuss_topic_cache", (
        "    `id` INT NOT NULL,\n"
        "    `first_reply_id` INT NOT NULL,\n"
        "    `last_reply_id` INT NOT NULL,\n"
        "    PRIMARY KEY(`id`)\n"
        )
    ),
    ("discuss_reply", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `tid` INT NOT NULL,\n"
        "    `uid` INT NOT NULL,\n"
        "    `reply_to_id` INT NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    `text` TEXT NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("notice", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `from_uid` INT NOT NULL,\n"
        "    `to_uid` INT NOT NULL,\n"
        "    `item_id` INT NOT NULL,\n"
        "    `type` VARCHAR(20) NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    `isRead` TINYINT(1) NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("mail", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `from_uid` INT NOT NULL,\n"
        "    `to_uid` INT NOT NULL,\n"
        "    `title` VARCHAR(100) NOT NULL,\n"
        "    `text` TEXT NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    `isRead` TINYINT(1) NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("tag", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `content` VARCHAR(100) NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    PRIMARY KEY (`id`),\n"
        "    UNIQUE KEY(`content`)\n"
        )
    ),
    ("tag_cache", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `topic_count` INT NOT NULL,\n"
        "    `reply_count` INT NOT NULL,\n"
        "    PRIMARY KEY(`id`)\n"
        )
    ),
    ("discuss_topic_tag_bridge", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `topic_id` INT NOT NULL,\n"
        "    `tag_id` INT NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("focus", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `from_uid` INT NOT NULL,\n"
        "    `focus_type` ENUM('user', 'topic', 'tag') NOT NULL,\n"
        "    `target_id` INT NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    `is_del` BOOLEAN NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),

# action表应该是一个巨大的冗余。
# 暂时，设计及实现时仅考虑读取的方便，不考虑冗余问题
    ("action", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `from_object_id` INT NOT NULL,\n"
        "    `from_object_type` ENUM('user', 'topic', 'tag') NOT NULL,\n"
        "    `action_type` ENUM('focus', 'post', 'reply') NOT NULL,\n"
        "    `target_object_id` INT NOT NULL,\n"
        "    `target_object_type`"
        "    ENUM('user', 'topic', 'tag', 'reply') NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
    ("usermsg", (
        "    `id` INT NOT NULL AUTO_INCREMENT,\n"
        "    `from_uid` INT NOT NULL,\n"
        "    `to_uid` INT NOT NULL,\n"
        "    `text` VARCHAR(200) NOT NULL,\n"
        "    `ctime` DATETIME NOT NULL,\n"
        "    PRIMARY KEY (`id`)\n"
        )
    ),
)


def layout(self):
    ''' 此页的布局 '''
    self.setTitle('数据库')


def create_tables(request):
    ''' 创建数据表 '''
    db_object = Db.singleton()
    table_prefix = db_object.table_prefix()

    result = []
    for table_name, table_sql in __tables__:
        sql = (
            'CREATE TABLE IF NOT EXISTS '
            '`%s%s`(\n%s)'
            'ENGINE=MyISAM DEFAULT CHARSET=utf8'
        ) % (
            table_prefix, table_name, table_sql
        )
        res = db_object.execute(sql)
        result.append({
            'table_name': table_name,
            'sql': sql,
            'res': res
        })

    return json_response(result)


def drop_tables(self):
    ''' 删除数据表 '''
    db_object = Db.singleton()
    table_prefix = db_object.table_prefix()

    result = []
    for table_name, _ in __tables__:
        sql = 'DROP TABLE IF EXISTS `%s%s`' % (
            table_prefix, table_name
        )
        res = db_object.execute(sql)
        result.append({
            'table_name': table_name,
            'sql': sql,
            'res': res,
        })

    self.set_variable('result', result)
