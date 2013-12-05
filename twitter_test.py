#!/usr/bin/env python2

import tweepy
import MySQLdb
import sys

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

    def get_tweets_from_user(self, user, cnt = 20):
        self.API.user_timeline(user, count=cnt)


consumerKey = 'jf1RuBnCqdQCNmLX0frLg'
consumerSecret = 'ThqOiemmb6u0unxovHEg9r9m4Lf0MaI30nqh3gwedI'
accessKey = '1106939719-KyTHxcGncJp0vgxTjH8P2AmaGQ13B5ert7YZR0t'
accessSecret = 'PqIuAYKTuKFfrg24CAhuwigh5R2udkl2Fls06mTaZLhXZ'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)
user = api.get_user("KingJames")
pub = api.home_timeline()
lebron_status = api.user_timeline("KingJames", count=5)
for status in lebron_status:
    print status.text

#!/usr/bin/python

if(True):
    # Open database connection
    db = MySQLdb.connect("localhost","root","","celebrity")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO celebrity\
           VALUES ('%i', '%s', '%s', '%s')" % \
           (1,'Lebron', 'James', 'KingJames')


    #Execute the SQL command
    cursor.execute(sql)
    t_id = 1
    for status in lebron_status:
        string = MySQLdb.escape_string(str(status.text[:255].encode("utf-8")))
        sql = "INSERT INTO tweets\
        VALUES ('%i', '%s', '%s')" % \
        (t_id,'KingJames',string)
        print sql
        cursor.execute(sql)
        t_id+=1;

        # Commit your changes in the database
    db.commit()

    #except:
    #    print "not successful"
        # Rollback in case there is any error
    #    db.rollback()
        # disconnect from server

    #db.close()
