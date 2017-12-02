import urllib
import urllib2
import re
import os


#Set up dictionaries mapping word to Valence Mean and Arousal Mean(pos/neg score)
f=open('anewtable1.txt')
l2=f.readlines()
valenced={}
arousald={}
for line in l2:
    a=line.split('\t')
    valenced[a[0]]=float(a[2])
    arousald[a[0]]=float(a[4])
f.close()


def spliceToList(string,head,tail):
    '''returns a list of strings which were bounded by head and tail in the original string'''
    out=[]
    a=string.partition(head)
    while 1:        
        if a[2]=='':
            break
        b=a[2].partition(tail)
        out.append(b[0])
        a=a[2].partition(head)
    return out

def spliceOut(string,out):
    '''removes every occurrence of out from string'''
    a=string.split(out)
    string=''
    for part in a:
        string+=part
    return string

def nextPageExt(source,head, tail):
    a=source.partition(tail)
    b=a[0].rpartition(head)
    return b[2]

def twitterScrape(searchterm,pages):
    #accessing twitter
    data={}
    data['q']=searchterm
    url_values=urllib.urlencode(data)
    opener=urllib2.build_opener()
    opener.addheaders=[('User-agent','Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.9) Gecko/2009040821 Firefox/3.0.9')]
    urllib2.install_opener(opener)

    url='http://search.twitter.com/search?'+url_values
    page=urllib2.urlopen(url)
    source=page.read().lower()
    n=1
    while n<=pages:
        try:
            url2='http://search.twitter.com'+spliceOut(nextPageExt(source,'<a href="','" class="next">older</a>'),'amp;')
            page2=urllib2.urlopen(url2)
            source2=page2.read().lower()
            source+=source2
            n+=1
        except:
            print 'no page '+str(n)
            break
    return source

    #processing source
def twitterScore(source,searchterm):
    s=searchterm.split(' ')
    for word in s:
        source=spliceOut(source,'<b>'+word+'</b>')
    msglist=spliceToList(source,'class="msgtxt en">','</span>')
    i=0
    sumofi=0
    for msg in msglist:
        n=0
        sumofn=0

        msg=re.sub('<.*>','',msg)
        msg=re.sub('\W',' ',msg)
        words=msg.split(' ')
        for word in words:
            if word in valenced:
                sumofn+=(valenced[word]-5.0)*arousald[word]
                n+=1
        if n!=0:
            sumofi+=sumofn/n
            i+=1

    if i!=0:
        value=float(sumofi)/i
    else:
        value=None
    
    f=open('scores.txt')
    a=f.readlines()
    f.close()
    
    searched=0
    oldvalue=0
    newvalue=value
    if a==[]:
        pass
    elif searchterm+'\n'==a[0]:
        searched=1
        oldvalue=float(a[1])
        newvalue=(oldvalue+value)/2.0
    a=[searchterm+'\n',str(newvalue)]
    os.remove('scores.txt')
    
    f=open('scores.txt','w')
    f.writelines(a)
    f.close()
    
    return newvalue

def TwitterSearch(searchterm,pages=10):
    searchterm=searchterm.lower()
    return twitterScore(twitterScrape(searchterm,pages),searchterm)
