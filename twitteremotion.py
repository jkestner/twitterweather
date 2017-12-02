# twitteremotion
# The heart of the system.
# Generates XML for Twitter terms. Also utility calls like trending topics.


import os, sys, time
#sys.stderr = sys.stdout

import tweepy

import cgi, urllib, urllib2
#import twitter
import simplebayes
import simplejson as json
from datetime import timedelta, date
from xml.dom.minidom import Document, parse
from threading import Thread

import servervar

auth = tweepy.OAuthHandler(servervar.TWITTER_CONSUMER_KEY, servervar.TWITTER_CONSUMER_SECRET)
auth.set_access_token(servervar.TWITTER_ACCESS_TOKEN_KEY, servervar.TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)


def getXML(query={}):
	search_terms = []
	search_scores = []
	search_scores_y = []
	search_scores_y1 = []
	search_scores_y2 = []
	search_scores_y3 = []
	
	if query.has_key("geocode"):
		return getXMLForGeocode(query)

	search_terms = termsList(query)
		
	# Create the minidom document
	doc = Document()
	
	# Create the base element
	tw = doc.createElement("twither")
	doc.appendChild(tw)
	
	f = urllib.urlopen('http://twitterweather.media.mit.edu/blank.html') # if we don't use urlopen before the threads, this crashes Python in Snow Leopard. http://bugs.python.org/issue6851

	for term in search_terms:
		if term is None or term == '':
			continue
		
		threaded_queries = []
		term = term.encode('utf-8')
		
		# check if there's already a results file that's recent
		termq = urllib.quote(term,'')
		if os.path.exists(servervar.CACHE_DIR+termq+'.xml') and time.time() - os.path.getmtime(servervar.CACHE_DIR+termq+'.xml') < servervar.REFRESH_PERIOD: #todo: should be looking across cache dirs. should this even be here and in the cgi?
			g = open(servervar.CACHE_DIR+termq+'.xml')
			maincard = parse(g).firstChild
			tw.appendChild(maincard)
			g.close()
		
		else:
			current = twitterScore(term)
			threaded_queries.append(current)
			current.start()

			start = (date.today()).strftime("%Y-%m-%d")
			end = (date.today() + timedelta(1)).strftime("%Y-%m-%d")
			current = twitterScore(term, start, end)
			threaded_queries.append(current)
			current.start()

			start = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
			end = (date.today()).strftime("%Y-%m-%d")
			current = twitterScore(term, start, end)
			threaded_queries.append(current)
			current.start()

			start = (date.today() - timedelta(2)).strftime("%Y-%m-%d")
			end = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
			current = twitterScore(term, start, end)
			threaded_queries.append(current)
			current.start()

			start = (date.today() - timedelta(3)).strftime("%Y-%m-%d")
			end = (date.today() - timedelta(2)).strftime("%Y-%m-%d")
			current = twitterScore(term, start, end)
			threaded_queries.append(current)
			current.start()


			for query in threaded_queries:
				query.join()


			# Create the main element
			maincard = doc.createElement("place")
			tw.appendChild(maincard)
			
			eterm = doc.createElement("term")
			maincard.appendChild(eterm)
			tterm = doc.createTextNode(cgi.escape(term))
			eterm.appendChild(tterm)
			
			scoreElements = ["score","score_today","score_1dayago","score_2daysago","score_3daysago"]
			for elName in scoreElements:
				escore = doc.createElement(elName)
				maincard.appendChild(escore)
				wscore = threaded_queries[scoreElements.index(elName)].score
				if wscore is not None:
					tscore = doc.createTextNode(str(wscore))
					escore.appendChild(tscore)


			# cache it
			g = open(servervar.CACHE_DIR+termq+'.xml','w')
			g.write( maincard.toprettyxml(indent="  ") )
			g.close()

		
	# Save/print our newly created XML
	xmldata = doc.toprettyxml(indent="  ")
	#doc.unlink()
	return xmldata


def getXMLForGeocode(query={},rlat=None,rlon=None):
	search_terms = []
	search_scores = []
	lat = None
	lon = None
	radius = '100km'
	
	search_terms = termsList(query)
	if query.has_key("lat"):
		lat = query.getfirst("lat")
	if rlat is not None:
		lat = str(rlat)
	if query.has_key("lon"):
		lon = query.getfirst("lon")
	if rlon is not None:
		lon = str(rlon)
	if query.has_key("radius"):
		radius = query.getfirst("radius")

		
	# Create the minidom document
	doc = Document()
	
	# Create the base element
	tw = doc.createElement("twither")
	doc.appendChild(tw)
	
	f = urllib.urlopen('http://localhost') # if we don't use urlopen before the threads, this crashes Python in Snow Leopard. http://bugs.python.org/issue6851

	for term in search_terms:
		threaded_queries = []
		term = term.encode('utf-8')
		
		# check if there's already a results file that's recent
		termq = urllib.quote(term,'')
		if os.path.exists(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml') and time.time() - os.path.getmtime(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml') < servervar.REFRESH_PERIOD:
			g = open(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml')
			maincard = parse(g).firstChild
			tw.appendChild(maincard)
			g.close()
		
		else:
			current = twitterScoreG(term, lat, lon, radius)
			threaded_queries.append(current)
			current.start()


			for query in threaded_queries:
				query.join()


			# Create the main element
			maincard = doc.createElement("place")
			maincard.setAttribute("lat", lat)
			maincard.setAttribute("lon", lon)
			maincard.setAttribute("radius", radius.strip('kmi'))
			tw.appendChild(maincard)
			
			eterm = doc.createElement("term")
			maincard.appendChild(eterm)
			#tterm = doc.createTextNode(term)
			tterm = doc.createTextNode(cgi.escape(term))
			eterm.appendChild(tterm)
			
			escore = doc.createElement("score")
			maincard.appendChild(escore)
			tscore = doc.createTextNode(str(threaded_queries[0].score))
			escore.appendChild(tscore)

			# cache it
			g = open(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml','w')
			g.write( maincard.toprettyxml(indent="  ") )
			g.close()

		
	# Save/print our newly created XML
	xmldata = doc.toprettyxml(indent="  ")
	#doc.unlink()
	return xmldata


def getGeocodeXML(query={}):
	search_terms = []
	search_scores = []
	radius = 500
	
	search_terms = termsList(query)
	if type(query) is cgi.FieldStorage and query.has_key("radius"):
		radius = int(query.getfirst("radius"))

		
	# Create the minidom document
	doc = Document()
	
	# Create the base element
	tw = doc.createElement("twither")
	doc.appendChild(tw)
	
	f = urllib.urlopen('http://localhost') # if we don't use urlopen before the threads, this crashes Python in Snow Leopard. http://bugs.python.org/issue6851

	for term in search_terms:
		term = term.encode('utf-8')
		termq = urllib.quote(term,'')
		threaded_queries = []
		
		# start threads
		for lat in range(25,55,radius/100):
			for lon in range(-125,-65,radius/100):
				lat = str(lat)
				lon = str(lon)
				# check if there's already a results file that's recent
				if os.path.exists(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml') and time.time() - os.path.getmtime(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml') < servervar.REFRESH_PERIOD*6*24:
					g = open(servervar.MAP_CACHE_DIR+lat+','+lon+'-'+termq+'.xml')
					print g.read()
#					maincard = parse(g).firstChild
#					tw.appendChild(maincard)
					g.close()
				
				else:
					current = twitterScoreG(term, lat, lon, radius)
					threaded_queries.append(current)
					current.start()
					#time.sleep(.2)

		# wait for threads to finish
		for query in threaded_queries:
			query.join()
			
			if query.score is None:
				continue

			# Create the main element
			maincard = doc.createElement("place")
			maincard.setAttribute("lat", query.lat)
			maincard.setAttribute("lon", query.lon)
			maincard.setAttribute("radius", str(query.radius))
			tw.appendChild(maincard)
			
			eterm = doc.createElement("term")
			maincard.appendChild(eterm)
			#tterm = doc.createTextNode(term)
			tterm = doc.createTextNode(cgi.escape(term))
			eterm.appendChild(tterm)
			
			escore = doc.createElement("score")
			maincard.appendChild(escore)
			tscore = doc.createTextNode(str(query.score))
			escore.appendChild(tscore)

			# cache it
			g = open('mapcache/'+query.lat+','+query.lon+'-'+termq+'.xml','w')
			g.write( maincard.toprettyxml(indent="  ") )
			g.close()

		
	# Save/print our newly created XML
	xmldata = doc.toprettyxml(indent="  ")
	#doc.unlink()
	return xmldata


# whether input is a form dictionary, list, or comma-separated string, return a list of terms
def termsList(query):
	if type(query) is list:
		return query
	if type(query) is str:
		return [q.strip() for q in query.split(',')]
	if query.has_key("search") and len(query.getfirst("search").strip()) > 0:
		return [q.strip() for q in query.getfirst("search").split(',')]
	else:
		return currentTrends()

# get current Twitter trends (caching)
def currentTrends():
	terms = []
	trends = []
	if os.path.exists(servervar.CACHE_DIR+'trends1.json') and time.time() - os.path.getmtime(servervar.CACHE_DIR+'trends1.json') < servervar.REFRESH_PERIOD:
		f = open(servervar.CACHE_DIR+'trends1.json')
		trends = json.load(f, 'utf-8')
	else: 
		trends = twitter_api.trends_location(woeid=1)
		g = open(servervar.CACHE_DIR+'trends1.json','w')
		g.write( json.dumps(trends) )
	

	bl = blockList()
	for item in trends[0]['trends']:
		#print repr(item['name'])
		#print item['name'].encode('unicode_escape')
		itemname = item['name'].replace(u'\u2019',u'\u0027') #remove nasty unicode curly single quotes
		itemname = item['name'].replace(u'\u2665',u'') #remove nasty unicode heart
		#itemname = itemname.encode('utf-8','ignore')
		#itemname = item['name'].encode('unicode_escape')
		
		ok = True
		for blockedtopic in bl:
			if blockedtopic.lower() in item['name'].lower():
				ok = False
				break
		if ok:
			terms.append(itemname)
			
	return terms
	
# get list of terms to filter out of trending topics
def blockList():
	import codecs
	f = codecs.open( "blocktopics.txt", "r", "utf-8" )
	l = f.read().split('\n')
	return l
	
	
class twitterScore(Thread):
	def __init__ (self,term,begin=None,end=None):
		Thread.__init__(self)
		self.term = term
		self.begin = begin
		self.end = end
		self.score = None
	def run(self):
		self.score = simplebayes.twitterHistoryScrapeT(self.term,self.begin,self.end)
		#return score

class twitterScoreG(Thread):
	def __init__ (self,term,lat,lon,radius):
		Thread.__init__(self)
		self.term = term
		self.lat = lat
		self.lon = lon
		self.radius = radius
		self.score = None
	def run(self):
		self.score = simplebayes.twitterLocationScrape(self.term,self.lat,self.lon,self.radius)
		#return score


if __name__ == '__main__':
	print getXML()
