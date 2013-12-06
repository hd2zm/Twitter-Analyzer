__author__ = 'user'

import tweepy
import MySQLdb
import sys

import DatabaseConnection

class TwitterReader:

    def __init__(self, consumerKey, consumerSecret, accessKey, accessSecret):
        self.cK = consumerKey
        self.cS = consumerSecret
        self.aK = accessKey
        self.aS = accessSecret
        self.auth = self.authorize()
        self.API = self.getAPI(self.auth)

    def authorize(self):
        auth = tweepy.OAuthHandler(self.cK, self.cS)
        auth.set_access_token(self.aK, self.aS)
        return auth

    def getAPI(self, auth):
        return tweepy.API(auth)

    def get_user(self, user):
        return self.API.get_user(user)

    def get_tweets_from_user(self, user, cnt):
        self.API.user_timeline(user, count=cnt)
