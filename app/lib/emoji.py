import emoji_list

def isEmoji(name):
	return (name in emoji_list.nameset)

if '__main__' == __name__:
	print isEmoji(u'100')
	print isEmoji('100')
	print isEmoji(u'200')
	print isEmoji(u'xxx')
