#!/usr/bin/python

# -----------------
# call with a query string of 'search' and the terms to search for, separated by comma
# call with a query string of 'url' to get the comment weather for supported sites
# call with a query string of 'xml' to get XML output instead of HTML
# if no search query is set, this will fetch the top 10 trending topics
# -----------------

import os, sys, codecs
sys.path.append("comments")

import cgi
import time, glob
from datetime import timedelta, date

import servervar
import twitteremotion, commentweather

from weatherreport import *
from xml.dom.minidom import Document

#sys.setdefaultencoding('utf_8')


if __name__ == '__main__':
	
	outputXML = False;

	form = cgi.FieldStorage()
	search_terms = []
	if form.has_key("output") and form.getfirst("output").lower() == "xml":
		outputXML = True;

		print "Content-Type: text/plain\n\n"

		# generate XML files for any requested terms, or current trends
		twitteremotion.getXML(form)
	
		# scan cache for anything updated in the last X minutes
		cache_files = []
		tagOpened = False
		
		li = filter(os.path.isfile, glob.glob('caches/*/*.xml')) #includes path
		li.sort(reverse=True,key=lambda x: os.path.getmtime(x))
	
		for f in li:
			fn = os.path.splitext(os.path.basename(f))[0] #we're going to render only cached files not (already displayed) in search terms 
			if time.time() - os.path.getmtime(f) < servervar.REFRESH_PERIOD:
				if not tagOpened:
					print '<?xml version="1.0" ?>'
					print '<twither>'
					tagOpened = True
	
				cache_files.append(f)
				g = open(f)
				print g.read()
				g.close()
		if tagOpened:
			print '</twither>'
	else:
		print "Content-Type: text/html\n"
		print '<?xml version="1.0" encoding="utf-8"?>'
		print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
		print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'
		print '<head>'
		print '<title>Recent weather reports</title>'
		print '<link rel="stylesheet" href="inc/widget.css" charset="utf-8" />'
		print '<meta http-equiv="refresh" content="600" />'
		print '</head>'
		print '<body class="inthesite">'
	
		print open('inc/weather_header.inc').read()
	
		# if any terms requested, generate their XML files
		if form.has_key("url"):
			url = form.getfirst("url")
			weatherForXML( commentweather.getXML(url) )
		else:
			if form.has_key("search"):
		#		print '<span class="requested">'
				weatherForXML( twitteremotion.getXML(form) )
				search_terms = twitteremotion.termsList(form)
		#		print '</span>'
		
			# scan cache for anything updated in the last X minutes
			cache_files = []
		
			li = filter(os.path.isfile, glob.glob('caches/*/*.xml')) #includes path
			li.sort(reverse=True,key=lambda x: os.path.getmtime(x))
		
			for f in li:
				fn = os.path.splitext(os.path.basename(f))[0] #we're going to render only cached files not (already displayed) in search terms 
				if time.time() - os.path.getmtime(f) < servervar.REFRESH_PERIOD and fn not in search_terms:
					cache_files.append(f)
					g = open(f)
					weatherForXML( g.read() )
					
					#todo: sort by last updated
			
			# if no recent queries, get current trends
#			if (not form.has_key("search") or form.getfirst("search") is None):
			if len(cache_files) == 0:
				weatherForXML( twitteremotion.getXML() ) #todo: filter out dupes
	
		print '</body></html>'
