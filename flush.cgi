#!/usr/bin/python
import os
import time
import sys
from threading import Thread
import simplebayes, urllib

class twitterScore(Thread):
   def __init__ (self,term):
      Thread.__init__(self)
      self.term = term
      self.status = -1
   def run(self):
      score = simplebayes.twitterHistoryScrapeT(self.term)
      print score

terms = ['Republicans','Democrats','Obama','Pelosi','Glenn Beck']
queryList = []

f = urllib.urlopen('http://mom.media.mit.edu') # if we don't use urlopen before the threads, this crashes Python in Snow Leopard. http://bugs.python.org/issue6851

for t in terms:
   current = twitterScore(t)
   queryList.append(current)
   current.start()

for query in queryList:
   query.join()
