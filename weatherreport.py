# weatherreport
# Generates an HTML weather view given an XML file

import sys
from urllib import quote
from xml.dom.minidom import parseString

import twitteremotion


def weather(term, url, score, score_history, source):
	term = term.encode("utf-8")
	termq = quote(term,'')
	if score is None:
		hcolor = '#999999'
		score = '?'
	else:
		hcolor = hexColor((100+score/5,80+score/0.7,150+score))
		score = int(score)
	
	if (score_history is None):
		placeDict = {'url': url, 'term': term, 'score': score, 'source': source, 'color': hcolor }
		f = open('inc/weather_template_article.inc')

	else:
		score_history = ['?' if sc is None  else sc  for sc in score_history]
	
		placeDict = {'url': url+termq,'term': term, 'score': score, 'score_y': score_history[0], 'score_y1': score_history[1], 'score_y2': score_history[2], 'score_y3': score_history[3], 'source': source, 'color': hcolor }
		f = open('inc/weather_template2.inc')

	# template will have placeholders in the format %(term)s for strings, %(score)d for integers, %(score_y).2f for floats

	print f.read() % placeDict
	sys.stdout.flush()

def hexColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def calculateScore(place,tagName):
	scoreNode = place.getElementsByTagName(tagName)[0]
	if not scoreNode.hasChildNodes():
		return None
	else:
		rawScore = scoreNode.childNodes[0].data.strip()
		if rawScore in u'None':
			return None
		return int(float(rawScore)*50+50)

def weatherForXML(xmlstring):
	dom = parseString( xmlstring )
	trends = twitteremotion.currentTrends()
	
	for place in dom.getElementsByTagName('place'):
		term = place.getElementsByTagName('term')[0].childNodes[0].data.strip()
		score = calculateScore(place,'score')

		# check for score history tags (different from not having a score)
		if len(place.getElementsByTagName('score_today')):
			score_y = calculateScore(place,'score_today')
			score_y1 = calculateScore(place,'score_1dayago')
			score_y2 = calculateScore(place,'score_2daysago')
			score_y3 = calculateScore(place,'score_3daysago')
			score_history = [score_y, score_y1, score_y2, score_y3]
		else:
			score_history = None
		if len(place.getElementsByTagName('url')):
			url = place.getElementsByTagName('url')[0].childNodes[0].data.strip()
		else:
			url = "http://search.twitter.com/search?q="
		if len(place.getElementsByTagName('source')):
			source = place.getElementsByTagName('source')[0].childNodes[0].data.strip()
		else:
			source = "Twitter"
		
		if score is None:
			scoreclass = 'none'
		else:
			scoreclass = str(int((score-.1)/20) + 1)
		print '<span class="score'+scoreclass+'">'
		
		weather(term, url, score, score_history, source)
					
		print '</span>'
		
	dom.unlink()
