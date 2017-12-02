import os, sys, time
sys.path.append("../")
import twitteremotion

import cgi, urllib, urllib2
import re
import simplebayes

from comments import Comments
from wsjcomments import WSJComments
from reuterscomments import ReutersComments
#from cnncomments import CNNComments
from weblogscomments import WeblogsComments
from disquscomments import DisqusComments


def main():
	if len(sys.argv) < 2:
		print "Need a URL as an argument"
	else:
		url = sys.argv[1]
		com = commentsObj(url)
		print com.weather()
		


def commentsObj(url):
	f = urllib.urlopen(url)
	pagesource = f.read()
	f.close()
	#print pagesource

	if 'disqus.com' in pagesource:
		return DisqusComments(url, pagesource)
	elif 'wsj.com/' in url:
		return WSJComments(url, pagesource)
	elif 'reuters.com/' in url:
		return ReutersComments(url, pagesource)
#	elif 'cnn.com/' in url:
#		return CNNComments(url, pagesource)
	return WeblogsComments(url, pagesource)



if __name__ == "__main__":
	main()