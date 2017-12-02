# simplebayes
# The backbone of the system. Scores terms based on retrieved tweets.
# Stephanie Bian


import urllib, urllib2
import re
import math
from datetime import timedelta, date
import simplejson as json

import servervar

def makeDicts():
    page=urllib2.urlopen('http://twitterweather.media.mit.edu/rating/pull.php')
    source=page.read()
    page.close()
    lines=re.split('<br>',source)
    wordsToRating=dict()
    for line in lines:
        if line!='':
            wordsRating=re.split(',',line)
            words=re.split('\s+',wordsRating[0])
            lowerwords=[]
            if wordsRating[1]!='0':
                for word in words:
                    if word!='':
                        lowerwords.append(word.lower())
                wordsToRating[tuple(lowerwords)]=int(wordsRating[1])

    posTweets=0
    nonposTweets=0
    posTweetsWithWord=dict()
    nonposTweetsWithWord=dict()
    for words in wordsToRating:
        temp=[]
        if wordsToRating[words]>0:
            posTweets+=1
            for word in words:
                if not word in temp:
                    temp.append(word)
                    if word in posTweetsWithWord:
                        posTweetsWithWord[word]+=1
                    else:
                        posTweetsWithWord[word]=1
        elif wordsToRating[words]<0:
            nonposTweets+=1
            for word in words:
                if not word in temp:
                    temp.append(word)
                    if word in nonposTweetsWithWord:
                        nonposTweetsWithWord[word]+=1
                    else:
                        nonposTweetsWithWord[word]=1
    return [posTweetsWithWord,nonposTweetsWithWord,posTweets,nonposTweets]
                        
def simpleBayes(text, posTweetsWithWord, nonposTweetsWithWord, posTweets, nonposTweets):
    text=re.sub('http://[^\s]+','',text)
    emoticons=re.findall('[:;=\)\(\[\]DP][-\'oO]?[:;=\)\(\[\]DP]|</?3',text)
    for emoticon in emoticons:
        text.replace(emoticon,' ')
    text=re.sub('[^a-zA-Z\s]','',text)
    
    w=re.split('\s+',text)
    b=0
    for word in w:
        if word!='':
            word=word.lower()
            if (word in posTweetsWithWord) and (word in nonposTweetsWithWord):
                b+=math.log(float(posTweetsWithWord[word])*nonposTweets/(nonposTweetsWithWord[word]*posTweets))

    for emoticon in emoticons:
        if re.search('.+\)|\(.+|.+\]|\[.+|.+D|<3',emoticon)!=None:
            b+=math.log(float(10))
        else:
            b+=math.log(1.0/10)
    a=math.log(float(posTweets)/nonposTweets)
    return a+b

# pass in a list of strings
def score(passages):
    if passages is None or len(passages) < servervar.MINIMUM_VOLUME:
        return None    # insufficient data

    score1=0
    d=makeDicts()
    posTweetsWithWords=d[0]
    nonposTweetsWithWords=d[1]
    posTweets=d[2]
    nonposTweets=d[3]
    for passage in passages:
        notags=re.sub('<.+?>.+?<\/.+?>','',passage)
        nopunct=re.sub('&amp;|&quot;|&apos;|&lt;|&gt;',' ',notags)
        bayes=simpleBayes(nopunct, posTweetsWithWords, nonposTweetsWithWords, posTweets, nonposTweets)
        if bayes>0:
            score1+=1
        elif bayes<0:
            score1-=1
    if len(passages) == 0:
        return 0
    return float(score1)/len(passages)


##def intensity(text):
##    page=urllib2.urlopen('http://scripts.mit.edu/~bian/pull.php')
##    source=page.read()
##    page.close()
##    lines=re.split('<br>',source)
##    wordsToRating=dict()
##    for line in lines:
##        if line!='':
##            wordsRating=re.split(',',line)
##            words=re.split('\s+',wordsRating[0])
##            lowerwords=[]
##            for word in words:
##                if word!='':
##                    lowerwords.append(word.lower())
##            wordsToRating[tuple(lowerwords)]=int(wordsRating[1])
##

def twitterHistoryScrape(searchterm, start=None, end=None):
    '''input search term and # pages of results, output is an averaged bayesian "score"'''
    data={}
    data['q']=searchterm
    data['rpp']=100
    # if dates are blank, it will show the latest tweets
    if start is not None:
        data['since']=start
    if end is not None:
        data['until']=end
    data['lang']='en'
    url_values=urllib.urlencode(data)
    opener=urllib2.build_opener()
    opener.addheaders=[('User-agent','Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.9) Gecko/2009040821 Firefox/3.0.9')]
    urllib2.install_opener(opener)

    tweets = []
    historyUrl = 'http://search.twitter.com/search.json?'+url_values

    f = urllib2.urlopen(historyUrl)
    yesterdaysTweets = json.load(f, 'utf-8')
    for item in yesterdaysTweets['results']:
        #print repr(item['text'])
        #print item['text'].encode('unicode_escape')
        #itemname = item['name'].replace(u'\u2019',u'\u0027') #remove nasty unicode curly single quotes
        tweets.append(item['text'].encode('unicode_escape'))

    return score(tweets)

def twitterHistoryScrapeT(searchterm, start=None, end=None):
    '''input search term and # pages of results, output is an averaged bayesian "score"'''
    data={}
    data['q']=searchterm
    data['rpp']=100
    # if dates are blank, it will show the latest tweets
    data['lang']='en'
    if start is not None:
        data['since']=start
    if end is not None:
        data['until']=end
    url_values=urllib.urlencode(data)
    #url_values='q='+searchterm

    tweets = []
    historyUrl = 'http://search.twitter.com/search.json?'+url_values

    f = urllib.urlopen(historyUrl)
    yesterdaysTweets = json.load(f, 'utf-8')
    for item in yesterdaysTweets['results']:
        #print repr(item['text'])
        #print item['text'].encode('unicode_escape')
        #itemname = item['name'].replace(u'\u2019',u'\u0027') #remove nasty unicode curly single quotes
        tweets.append(item['text'].encode('unicode_escape'))

    return score(tweets)


def twitterLocationScrape(searchterm, lat, lon, radius=100):
    '''input search term and # pages of results, output is an averaged bayesian "score"'''
    data={}
    data['q']=searchterm
    data['rpp']=100
    # if dates are blank, it will show the latest tweets
    data['lang']='en'
    data['geocode']=str(lat)+','+str(lon)+','+str(radius)+'km'
#    if start is not None:
#        data['since']=start
#    if end is not None:
#        data['until']=end
    url_values=urllib.urlencode(data)
    #url_values='q='+searchterm

    tweets = []
    historyUrl = 'http://search.twitter.com/search.json?'+url_values

    f = urllib.urlopen(historyUrl)
#    yesterdaysTweets = json.load(f, 'utf-8')
    try:
        yesterdaysTweets = json.load(f, 'utf-8')
    except ValueError:
        print f.read()
        yesterdaysTweets = {} 
    if yesterdaysTweets.has_key('results'):
        for item in yesterdaysTweets['results']:
            #print item['text']
            tweets.append(item['text'].encode('unicode_escape'))

    return score(tweets)


class TwitterURLopener(urllib.FancyURLopener):
    version = "TwitterWeather/0.9 +http://twitterweather.media.mit.edu/"

urllib._urlopener = TwitterURLopener()
