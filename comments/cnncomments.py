from comments import Comments
import urllib
from BeautifulSoup import BeautifulSoup
import re

class CNNComments(Comments):
	
	def title(self):
		t = self.pagesource.partition('</title>')[0].partition('<title>')[2].partition(' -')[0].strip()
		return unicode(t, 'iso-8859-1').translate(Comments.upunct)
	
	def urlComments(self):
		return self.url
	
	def comments(self):
		f = urllib.urlopen(self.urlComments())
		soup = BeautifulSoup(f.read())
		s2 = soup.findAll(attrs={"class":"dsq-comment-message"})
		print len(s2)

		comments = []
		for item in s2:
			print type(item)
			c = item.findAll('div')[1].string # get second, expanded comment
			if not c is None:
				c = re.split('[\.\?!] ',c)   # split by sentence for scoring
				comments.extend( c )
			
		return comments