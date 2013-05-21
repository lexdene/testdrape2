# -*- coding: utf-8 -*-

import markdown
import re
import time

import drape

@drape.util.utf8
def timeStamp2Str(t):
	return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t))

@drape.util.utf8
def timeStamp2Short(t):
	now = time.localtime()
	sti = time.localtime(t)
	
	if now.tm_year != sti.tm_year:
		return time.strftime('%Y-%m-%d',sti)
	elif now.tm_mon != sti.tm_mon or now.tm_mday != sti.tm_mday:
		return time.strftime('%m月%d日',sti)
	else:
		return time.strftime('%H:%M',sti)
