# -*- coding: utf-8 -*-

import markdown
import re
import time

import drape

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

def transText(text):
	if text is None:
		return ''
	text = markdown.markdown(text,safe_mode='escape')
	imgbasepath = 'https://a248.e.akamai.net/assets.github.com/images/icons/emoji'
	text = emoji(text,imgbasepath)
	return text

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
