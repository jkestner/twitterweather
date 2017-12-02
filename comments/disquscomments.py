from comments import Comments
import urllib
from xml.dom.minidom import Document, parse, parseString
import re, string
import simplejson as json

# feed://engadget2.disqus.com/t_mobile_g2_pre_orders_go_live_for_current_customers_available_to_all_on_october_6/latest.rss
# http://www.engadget.com/2010/09/24/t-mobile-g2-pre-orders-go-live-for-current-customers-available/

class DisqusComments(Comments):
	
	def title(self):
		return self.pagesource.partition('</title>')[0].partition('<title>')[2].rpartition(' --')[0].partition(' &emdash')[0]
	
	def urlComments(self):
		# extract subdomain for rss feed
		# known problem: generating disqus articleId (title) from page title. breaks if page title updated.
		
		subdomain = re.findall('http://([-a-z0-9]*)\.disqus\.com',self.pagesource)[0]

#		articleId = self.title().lower()
#		articleId = articleId.replace(' -- ',' ')
#		articleId = articleId.replace('-',' ')
#		articleId = articleId.translate(string.maketrans("",""), string.punctuation)
#		articleId = articleId.replace(' ','_')

		#urlComments = "http://" + subdomain + ".disqus.com/" + articleId + "/latest.rss"
		urlComments = "http://" + subdomain + ".disqus.com/thread.js?url=" + self.url
		return urlComments
	
	def comments(self):
		f = urllib.urlopen(self.urlComments())
		try:
			jobj = f.read().partition("/* */ jsonData = ")[2].partition("; /* */")[0];
			dom = json.loads(jobj, 'utf-8')
		except:
			return

		comments = []
		print len(dom["posts"])
		for msgId in dom["posts"]:
			c = dom["posts"][msgId]["message"]
			if c is None:
				continue
			c = re.split('[\.\?!] ',c.strip())   # split by sentence for scoring
			comments.extend( c )
	
		return comments