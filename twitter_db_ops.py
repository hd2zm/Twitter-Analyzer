import sqlite3, hashlib
from datetime import datetime
import os
import re

class Singleton:
  def __init__(self, klass):
    self.klass = klass
    self.instance = None
  def __call__(self, *args, **kwds):
    if self.instance == None:
      self.instance = self.klass(*args, **kwds)
    return self.instance

@Singleton
class TwitterDbOps:
    def __init__(self, path):
        if not path:
            self.path = ".twitteranalyzer.db"
            pass
        else:
            self.path = os.path.join(self.path, '.twitteranalyzer.db')
        self.setup()

    def setup(self):
        self.drop_tables()
        self.db = sqlite3.connect(self.path)
        # Get a cursor object for operations
        self.cur = self.db.cursor()
        # A method to make sure that all our tables in the database are initialized and ready to go
        self.cur.execute("CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY ASC, tweet TEXT, date DATE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS hashtags(id INTEGER PRIMARY KEY ASC, tweet id INTEGER, hashtag TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS reference(id INTEGER PRIMARY KEY ASC, tweet id INTEGER, reference TEXT)")
        # before exiting method
        self.db.commit()

    def drop_tables(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def hashtagExists(self, hashtag):
        self.cur.execute('SELECT * FROM hashtags WHERE hashtag=?',[hashtag])
        result  = self.cur.fetchall()
        if(len(result) > 0):
            return True
        else:
            return False

    def referenceExists(self, reference):
        self.cur.execute('SELECT * FROM reference WHERE reference=?',[reference])
        result  = self.cur.fetchall()
        if(len(result) > 0):
            return True
        else:
            return False

    def createTweet(self, tweet, date):
        self.cur.execute("INSERT INTO tweets VALUES(?,?,?)",[None,tweet,date])
        self.db.commit()

        self.cur.execute('SELECT id FROM tweets WHERE tweet=?',[tweet])
        tweetid = self.cur.fetchone()[0]
        #print tweetid

        self.createHashtag(tweetid, tweet)
        self.createReference(tweetid,tweet)

    def createHashtag(self,tweetid, tweet):
        for reg in re.findall('#\w*',tweet):
            self.cur.execute("INSERT INTO hashtags VALUES(?,?,?)",[None,tweetid,reg])
        self.db.commit()

    def createReference(self,tweetid, tweet):
        for reg in re.findall('@\w*',tweet):
            self.cur.execute("INSERT INTO reference VALUES(?,?,?)",[None,tweetid,reg])
        self.db.commit()

    def getTweets(self, count,hasCount):
        if not hasCount:
            self.getTweetsNoCount()
        if count < 0:
            count = 0
        self.cur.execute("SELECT * FROM tweets ORDER BY date DESC LIMIT ?",[count])
        return self.cur.fetchall()

    def getTweetsNoCount(self):
        self.cur.execute("SELECT * FROM tweets ORDER BY date DESC")
        return self.cur.fetchall()

    def getDates(self):
        self.cur.execute("SELECT date from tweets ORDER BY date DESC")

    def getHashtags(self):
        self.cur.execute("SELECT * FROM hashtags")
        return self.cur.fetchall()

    def getReferences(self):
        self.cur.execute("SELECT * FROM reference")
        return self.cur.fetchall()
