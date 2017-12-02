import sys
sys.path.append("../")

import urllib
import simplebayes


class Comments(object):
	
	upunct = {0x92:0x27}

	def __init__(self, url, pagesource=None):
		self.url = url
		if pagesource is None:
			f = urllib.urlopen(url)
			pagesource = f.read()
			f.close()
		self.pagesource = pagesource


	def title(self):
		raise NotImplementedError( "Need to implement this" )
	
	def urlComments(self):
		raise NotImplementedError( "Need to implement this" )
	
	def comments(self):
		raise NotImplementedError( "Need to implement this" )

	def weather(self):
		return self.title(), simplebayes.score(self.comments())
