import os, sys, time
import twitteremotion

import cgi, urllib, urllib2
import re
import simplebayes
import simplejson as json
from datetime import timedelta, date
from xml.dom.minidom import Document, parse, parseString
from threading import Thread

from comments import Comments
from wsjcomments import WSJComments
from reuterscomments import ReutersComments
#from cnncomments import CNNComments
from weblogscomments import WeblogsComments
from disquscomments import DisqusComments


import servervar

def getXML(articleURL):

	com = commentsObj(articleURL)
	
	
	atitle = com.title()
	if atitle is None:
		return
		
	# Create the minidom document
	doc = Document()
	
	# Create the base element
	tw = doc.createElement("twither")
	doc.appendChild(tw)
	
	f = urllib.urlopen('http://twitterweather.media.mit.edu/blank.html') # if we don't use urlopen before the threads, this crashes Python in Snow Leopard. http://bugs.python.org/issue6851

	# check if there's already a results file that's recent
	termq = urllib.quote(atitle,'&')
	if os.path.exists(servervar.CACHE_DIR+termq+'.xml') and time.time() - os.path.getmtime(servervar.CACHE_DIR+termq+'.xml') < servervar.REFRESH_PERIOD:
		g = open(servervar.CACHE_DIR+termq+'.xml')
		maincard = parse(g).firstChild
		tw.appendChild(maincard)
		g.close()
	
	else:
		weather = com.weather() # tuple title,score
		if weather is None:
			return
	
		asource = articleURL.split('/')[2] # get domain name out of URL
		
		# Create the main element
		maincard = doc.createElement("place")
		tw.appendChild(maincard)
		
		eterm = doc.createElement("term")
		maincard.appendChild(eterm)
		tterm = doc.createTextNode(cgi.escape(atitle))
		eterm.appendChild(tterm)
		
		escore = doc.createElement("score")
		maincard.appendChild(escore)
		if weather[1] is not None:
			tscore = doc.createTextNode( str(weather[1]) )
			escore.appendChild(tscore)

		eterm = doc.createElement("source")
		maincard.appendChild(eterm)
		tterm = doc.createTextNode(asource)
		eterm.appendChild(tterm)
		
		eterm = doc.createElement("url")
		maincard.appendChild(eterm)
		tterm = doc.createTextNode(cgi.escape(articleURL))
		eterm.appendChild(tterm)
		
		# cache it
		g = open(servervar.CACHE_DIR+termq+'.xml','w')
		g.write( maincard.toprettyxml(indent="  ") )
		g.close()

		
	# Save/print our newly created XML
	xmldata = doc.toprettyxml(indent="  ")
	#doc.unlink()

	return xmldata


def commentsObj(url):

	f = urllib.urlopen(url)
	pagesource = f.read()
	f.close()

	if 'disqus.com' in pagesource:
		return DisqusComments(url, pagesource)
	elif 'wsj.com/' in url:
		return WSJComments(url, pagesource)
	elif 'reuters.com/' in url:
		return ReutersComments(url, pagesource)
#	elif 'cnn.com/' in url:
#		return CNNComments(url, pagesource)
	return WeblogsComments(url, pagesource)
