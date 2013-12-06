__author__ = 'venkat'

import tweepy
from twython import *
from twitter_db_ops import DbOps
import MySQLdb
import sys

class TwitterReader:

    def __init__(self, consumerKey, consumerSecret, accessKey, accessSecret):
        self.cK = consumerKey
        self.cS = consumerSecret
        self.aK = accessKey
        self.aS = accessSecret
        self.twitter = Twython(self.cK, self.cS, self.aK, self.aS)
        #self.dbops = DBOps()

    def getAPI(self, auth):
        return self.twitter

    def get_user(self, user):
        return self.API.get_user(user)

    def get_tweets_from_user(self, user, cnt=20):
        suser = self.twitter.show_user(screen_name=user)
        if(cnt > suser['statuses_count']):
            cnt = suser['statuses_count']
        #3000 is the rate limit for twitter API - 15 calls in 15 minutes (200 tweets per call)
        if(cnt > 3000):
            cnt = 3000
        tweets_requested = []
        if cnt <= 200:
            timeline = self.twitter.get_home_timeline(screen_name=user, count=cnt)
            for tweet in timeline:
                tweets_requested.append(tweet)
                #self.dbops.createTweet(tweet['text'], tweet[''])
        elif cnt > 200:
            number_of_tweets = 0
            cntleft = cnt
            while(number_of_tweets < cnt):
                if cntleft>200:
                    cntleft-=200
                    timeline = self.twitter.get_home_timeline(screen_name=user, count=200, max_id=lowest_id)
                else:
                    timeline = self.twitter.get_home_timeline(screen_name=user, count=cntleft, max_id=lowest_id)
                for tweet in timeline:
                    number_of_tweets+=1
                    if tweet['id'] < lowest_id:
                        lowest_id = tweet['id']
                    tweets_requested.append(tweet)
                    #self.dbops.createTweet(tweet['text'], tweet['created_at'])
                lowest_id -= 1
        else:
            print "something strange happned"
        return tweets_requested

    def parse_date(self, date):
        pass