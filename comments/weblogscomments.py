from comments import Comments
import urllib
from xml.dom.minidom import Document, parse, parseString
import re

class WeblogsComments(Comments):
	
	def title(self):
		return self.pagesource.partition('</title>')[0].partition('<title>')[2].partition(' --')[0].partition(' &emdash')[0]
	
	def urlComments(self):
		urlComments = self.url
		if not urlComments.endswith('/'):
			urlComments += '/'
		urlComments += "comments.xml"
		return urlComments
	
	def comments(self):
		f = urllib.urlopen(self.urlComments())
		try:
			dom = parseString( f.read() )
		except:
			return
		
		comments = []
		for item in dom.getElementsByTagName('item'):
			c = item.getElementsByTagName('description')[0].childNodes[0].data.strip()
			c = re.split('[\.\?!] ',c)   # split by sentence for scoring
			comments.extend( c )
			
		dom.unlink()
	
		return comments