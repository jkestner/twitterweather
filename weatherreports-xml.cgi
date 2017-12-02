#!/usr/bin/python

# -----------------
# call with a query string of 'search' and the terms to search for, separated by comma
# if no search query is set, this will fetch the top 10 trending topics
# -----------------

import os, sys, codecs
sys.path.append("comments")

import cgi
import time, glob
from datetime import timedelta, date

import servervar
import twitteremotion, commentweather

from xml.dom.minidom import Document


if __name__ == '__main__':
	
	form = cgi.FieldStorage()
	search_terms = []

	print "Content-Type: text/plain\n\n"

	# generate XML files for any requested terms, or current trends
	twitteremotion.getXML(form)

	# scan cache for anything updated in the last X minutes
	cache_files = []
	tagOpened = False
	
	li = filter(os.path.isfile, glob.glob(servervar.CACHE_DIR+'/*.xml')) #includes path
	li.sort(reverse=True,key=lambda x: os.path.getmtime(x))

	for f in li:
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
