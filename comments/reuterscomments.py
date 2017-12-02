from comments import Comments
import urllib
from BeautifulSoup import BeautifulSoup
import re

class ReutersComments(Comments):
	
	def title(self):
		t = self.pagesource.partition('</title>')[0].partition('<title>')[2].partition(' |')[0].strip()
		return unicode(t, 'iso-8859-1').translate(Comments.upunct)
	
	def urlComments(self):
		urlParts = self.url.partition('article/')
		return urlParts[0] + urlParts[1] + "comments/" + urlParts[2]
	
	def comments(self):
		f = urllib.urlopen(self.urlComments())
		soup = BeautifulSoup(f.read())
		s2 = soup.findAll(attrs={"class":"commentsBody"})

		comments = []
		for item in s2:
			s3 = item.findAll('p')
			for itemP in s3:
				c = itemP.string
				if not c is None:
					c = re.split('[\.\?!] ',c)   # split by sentence for scoring
					comments.extend( c )
	
		return comments