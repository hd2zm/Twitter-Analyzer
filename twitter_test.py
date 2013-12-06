#!/usr/bin/env python2

import tweepy
import MySQLdb
import sys

import DatabaseConnection
import TwitterReader

from twython import Twython



consumerKey = 'jf1RuBnCqdQCNmLX0frLg'
consumerSecret = 'ThqOiemmb6u0unxovHEg9r9m4Lf0MaI30nqh3gwedI'
accessKey = '1106939719-KyTHxcGncJp0vgxTjH8P2AmaGQ13B5ert7YZR0t'
accessSecret = 'PqIuAYKTuKFfrg24CAhuwigh5R2udkl2Fls06mTaZLhXZ'

user = 'KingJames'

from TwitterReader import *
tw = TwitterReader(consumerKey,consumerSecret,accessKey,accessSecret)
lebron_status = (tw.getAPI(tw.auth)).user_timeline(user, count=5)


TWITTER_APP_KEY = 'jf1RuBnCqdQCNmLX0frLg' #supply the appropriate value
TWITTER_APP_KEY_SECRET = 'ThqOiemmb6u0unxovHEg9r9m4Lf0MaI30nqh3gwedI'
TWITTER_ACCESS_TOKEN = '1106939719-KyTHxcGncJp0vgxTjH8P2AmaGQ13B5ert7YZR0t'
TWITTER_ACCESS_TOKEN_SECRET = 'PqIuAYKTuKFfrg24CAhuwigh5R2udkl2Fls06mTaZLhXZ'

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

search = t.search(q='#YOLO',   #**supply whatever query you want here**
                 count=100)

tweets = search['statuses']

for tweet in tweets:
  print tweet['id_str'], '\n', tweet['text'], '\n\n\n'

#b = False
##!/usr/bin/python
#
#if(b):
#    # Open database connection
#    from DatabaseConnection import *
#    db = DatabaseConnection.connection
#
#    # prepare a cursor object using cursor() method
#    cursor = db.cursor()
#
#    # Prepare SQL query to INSERT a record into the database.
#    sql = "INSERT INTO celebrity\
#           VALUES ('%i', '%s', '%s', '%s')" % \
#           (1,'Lebron', 'James', 'KingJames')
#
#
#    #Execute the SQL command
#    cursor.execute(sql)
#    t_id = 1
#    for status in lebron_status:
#        string = MySQLdb.escape_string(str(status.text[:255].encode("utf-8")))
#        sql = "INSERT INTO tweets\
#        VALUES ('%i', '%s', '%s')" % \
#        (t_id,user,string)
#        print sql
#        cursor.execute(sql)
#        t_id+=1;
#
#        # Commit your changes in the database
#    db.commit()
#
#    #except:
#    #    print "not successful"
#        # Rollback in case there is any error
#    #    db.rollback()
#        # disconnect from server
#
#    db.close()
