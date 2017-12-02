from comments import Comments
import urllib
from BeautifulSoup import BeautifulSoup
import re
import cgi

class FoxNewsComments(Comments):
	
	def title(self):
		t = self.pagesource.partition('</title>')[0].partition('<title>')[2].partition(' |')[0].strip()
		print ">"+t+"<"
		return cgi.escape(unicode(t, 'iso-8859-1').translate(Comments.upunct))
	
	def urlComments(self):
		return self.url
	
	def comments(self):
		f = urllib.urlopen(self.urlComments())
		soup = BeautifulSoup(f.read()).find(attrs={"class":"comments-left"})
		s2 = soup.findAll('div',attrs={"class":"discussion"})

		comments = []
		for item in s2:
			s3 = item.findAll('p')
			for itemP in s3:
				c = itemP.string
				if not c is None:
					c = re.split('[\.\?!] ',c)   # split by sentence for scoring
					comments.extend( c )
	
		return comments