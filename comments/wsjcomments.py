from comments import Comments
import urllib
from xml.dom.minidom import Document, parse, parseString
import re

class WSJComments(Comments):
	
	def title(self):
		t = self.pagesource.partition('</title>')[0].partition('<title>')[2].partition(' -')[0].strip()
		return unicode(t, 'iso-8859-1').translate(Comments.upunct)
	
	def urlComments(self):
		if "online.wsj.com" in self.url:
			articleUri = self.url.partition('wsj.com/article/')[2].partition('.html')[0]
			return 'http://online.wsj.com/community/rss/storycomments.sync?subjectUri='+articleUri
		return self.url + "wp-commentsrss2.php" #ref http://codex.wordpress.org/Customizing_Feeds
	
	def comments(self):
		f = urllib.urlopen(self.urlComments())
		try:
			dom = parseString( f.read() )
		except:
			return
		
		comments = []
		for item in dom.getElementsByTagName('item'):
			if "online.wsj.com" in self.url:
				c = item.getElementsByTagName('count')[0].firstChild.data.strip()
			else:
				# filtering corruption of feed by comments from other articles
				comUrl = item.getElementsByTagName('link')[0].firstChild.data.rsplit('#',1)[0]
				if comUrl != self.url:
					continue
				c = item.getElementsByTagName('description')[0].firstChild.data.strip()
			c = re.split('[\.\?!] ',c)   # split by sentence for scoring
			comments.extend( c )
			
		dom.unlink()
	
		return comments