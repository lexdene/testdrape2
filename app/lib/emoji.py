import bisect
import emoji_list

def bin_search(a, x):
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return True
    return False

def isEmoji(name):
	return bin_search(emoji_list.namelist,name)

if '__main__' == __name__:
	print isEmoji(u'100')
	print isEmoji('100')
	print isEmoji(u'200')
	print isEmoji(u'xxx')
