#!/usr/bin/python

# -----------------
# call with a query string of 'search' and the terms to search for, separated by comma
# if no search query is set, this will fetch the top 10 trending topics
# -----------------

import os, sys, codecs
sys.path.append("comments")

import cgi, urllib, urllib2
import time, glob
from datetime import timedelta, date

import servervar

import commentweather
from weatherreport import *

#sys.setdefaultencoding('utf_8')


if __name__ == '__main__':
	
	form = cgi.FieldStorage()
	search_terms = []
	
	print "Content-Type: text/html\n"
	print '<?xml version="1.0" encoding="utf-8"?>'
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
	print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'
	print '<head>'
	print '<title>Recent weather reports</title>'
	print '<link rel="stylesheet" href="inc/widget.css" charset="utf-8" />'
	print '<meta http-equiv="refresh" content="600" />'
	print '</head>'
	print '<body>'

	print open('inc/weather_header.inc').read()

	if form.has_key("url"):
		url = form.getfirst("url")
		weatherForXML( commentweather.getXML(url) )
	else:
		# scan cache for anything updated in the last X minutes
		cache_files = []
	
		li = filter(os.path.isfile, glob.glob(servervar.COMMENT_CACHE_DIR+'*.xml')) #includes path
		li.sort(reverse=True,key=lambda x: os.path.getmtime(x))
	
		for f in li:
			fn = os.path.splitext(os.path.basename(f))[0] #we're going to render only cached files not (already displayed) in search terms 
			if time.time() - os.path.getmtime(f) < servervar.REFRESH_PERIOD and fn not in search_terms:
				cache_files.append(f)
				g = open(f)
				weatherForXML( g.read() )
				
				#todo: sort by last updated

	print '</body></html>'
