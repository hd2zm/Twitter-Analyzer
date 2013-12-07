__author__ = 'owner'
__faggot__ = 'venkat'

from Tkinter import *
from ttk import Frame, Style
import twitter_db_ops
from idlelib.WidgetRedirector import WidgetRedirector
import tkMessageBox
from PIL import ImageTk
import subprocess
import threading
import Queue
import os
from re import *
from twitter_interface import *
from twitter_reader import *
from twitter_db_ops import *
from datetime import datetime
import bar_graph
import line_graph

# The main class for this module. This class is the controller and defines the behaviours.
class SInterface():

    def __init__(self):
        # This is the model. The db class is a wrapper around database operations.
        self.dbops = TwitterDbOps("")
        self.root =Tk()
        self.root.geometry("1150x400+100+100")

        '''
        self.consumerKey = 'IFycAuEiZOo7mNOmNuW1lw'
        self.consumerSecret = 'E8MuIeoAKEWhLfbVDJAYyVL5sw9XIlEIbchqIotjxsE'
        self.accessKey = '35871247-89JyKTkbtn9L9V4fmkMMD7qHuOE39leWxJunutcSn'
        self.accessSecret = 'c6lxvaPOStYBWplXGZdW0AbhL00bMwVDReJflOc902fxg'
        '''
        self.consumerKey = 'jf1RuBnCqdQCNmLX0frLg'
        self.consumerSecret = 'ThqOiemmb6u0unxovHEg9r9m4Lf0MaI30nqh3gwedI'
        self.accessKey = '1106939719-KyTHxcGncJp0vgxTjH8P2AmaGQ13B5ert7YZR0t'
        self.accessSecret = 'PqIuAYKTuKFfrg24CAhuwigh5R2udkl2Fls06mTaZLhXZ'

        self.tweetReader = TwitterReader(self.consumerKey,self.consumerSecret,self.accessKey,self.accessSecret)

        self.view = View(self.root, self)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def verifyUsername(self):
        self.valid = False
        if self.tweetReader.lookup_user(self.view.username.get()):
            self.view.username.config(bg='green')
            self.view.appendText("User: %s is valid!" %self.view.username.get())
            #self.valid = True
        else:
            self.view.username.config(bg='red')
        self.view.appendLine()


    def getTweets(self):
        try:
            if self.valid:
                try:
                    self.dbops.setup()
                    tweets=self.tweetReader.get_tweets_from_user(self.view.username.get(),int(self.view.numTweets.get()))
                    self.tweetsToDB(tweets)
                    #self.view.appendText(str(len(tweets)))
                except TwitterReaderException:
                    self.view.appendText("Rate Limit Exceeded; Please wait 15 minutes.")
        except AttributeError:
            self.view.appendText("Please enter and verify a user.")

    def listTweets(self):
        #print self.view.numTweets.get()
        tweets = self.dbops.getTweets(self.view.numTweets.get())
        if not self.view.numTweets.get()=='' and int(self.view.numTweets.get()) > len(tweets):
            self.view.appendText("There are only %d tweets in the database" %(len(tweets)))
            return
        tweets = self.date_filter(tweets)
        for tweet in tweets:
            self.view.appendText(tweet[2])
            self.view.appendText(tweet[1] + "\n")
        self.view.appendLine()

    def mostHash(self):
        hashes = self.getHastagsCount(self.view.numTweets.get())
        hashdict = {}
        hasharray = []
        graph_hashes = []
        graph_hash_frequencies = []
        num_bars = 5
        if num_bars > self.view.numTweets.get():
            num_bars = self.view.numTweets.get()
        if hashes == None:
            return
        for hash in hashes:
            if hash[2].lower() in hashdict:
                hashdict[hash[2].lower()]= hashdict[hash[2].lower()]+1
            else:
                hashdict[hash[2].lower()] = 1
        for hashtag in hashdict:
            hasharray.append((hashdict[hashtag],hashtag))
        hasharray.sort(reverse=True)
        self.view.appendText("Most Used Hashtags:")
        for n in hasharray:
            self.view.appendText('%s used %d times'%(n[1],n[0]))
        self.view.appendLine()
        for x in range(num_bars):
            graph_hashes.append(hasharray[x][1])
            graph_hash_frequencies.append(hasharray[x][0])
        hash_bar_graph = bar_graph.BarGraph()
        hash_bar_graph.plot(graph_hash_frequencies, graph_hashes, "most used hashtags")

    def timeGraph(self):
        tweets = self.dbops.getTweets(self.view.numTweets.get(),not not self.view.numTweets.get())
        if not not self.view.numTweets.get() and int(self.view.numTweets.get()) > len(tweets):
            self.view.appendText("There are only %d tweets in the database" %(len(tweets)))
            return
        tweets = self.date_filter(tweets)
        tweetdict = {}
        tweetarray = []

        if tweets == None:
            return

        for tweet in tweets:
            day = datetime.strptime(tweet[2], '%Y-%m-%d %H:%M:%S')
            day  = datetime(day.year,day.month,day.day)
            if day in tweetdict:
                tweetdict[day]= tweetdict[day]+1
            else:
                tweetdict[day] = 1
        for n in tweetdict:
            tweetarray.append((n,tweetdict[n]))
        tweetarray.sort()
        days = []
        freq = []
        for n in tweetarray:
            days.append(n[0])
            freq.append(n[1])
        lg = line_graph.LineGraph()
        lg.plot(days,freq)

    def communicated(self):
        refers = self.getReferenceCount(self.view.numTweets.get())
        refdict = {}
        refarray = []
        graph_reference_frequencies = []
        graph_references = []
        num_bars = 5
        if num_bars > self.view.numTweets.get():
            num_bars = self.view.numTweets.get()
        if refers == None:
            return

        for refer in refers:
            if refer[2].lower() in refdict:
                refdict[refer[2].lower()]= refdict[refer[2].lower()]+1
            else:
                refdict[refer[2].lower()] = 1
        for n in refdict:
            refarray.append((refdict[n],n))
        refarray.sort(reverse=True)
        self.view.appendText("Most Used References:")
        for n in refarray:
            self.view.appendText('%s used %d times'%(n[1],n[0]))
        self.view.appendLine()
        for x in range(num_bars):
            graph_references.append(refarray[x][1])
            graph_reference_frequencies.append(refarray[x][0])
        reference_bar_graph = bar_graph.BarGraph()
        reference_bar_graph.plot(graph_reference_frequencies, graph_references, "most used references")

    def tweetsToDB(self,tweets):
        tweet_count = 1
        for tweet in tweets:
            self.dbops.createTweet(tweet['text'], self.tweetReader.parse_date(tweet['created_at']))
            tweet_count+=1


    def getHastagsCount(self,count):
        if not count:
            count ='3000'
        tweets = self.dbops.getTweets(count)
        if not self.view.numTweets.get()=='' and int(self.view.numTweets.get()) > len(tweets):
            self.view.appendText("There are only %d tweets in the database" %(len(tweets)))
            return
        tweets = self.date_filter(tweets)
        hashes = self.dbops.getHashtags()
        countedHashes = []

        for tweet in tweets:
            for hash in hashes:
                if tweet[0] == hash[1]:
                    countedHashes.append(hash)
        return countedHashes

    def getReferenceCount(self,count):
        if not count:
            count ='3000'
        tweets = self.dbops.getTweets(count)
        if not self.view.numTweets.get()=='' and int(self.view.numTweets.get()) > len(tweets):
            self.view.appendText("There are only %d tweets in the database" %(len(tweets)))
            return
        tweets = self.date_filter(tweets)
        refers = self.dbops.getReferences()
        countedRefers = []

        for tweet in tweets:
            for refer in refers:
                if tweet[0] == refer[1]:
                    countedRefers.append(refer)
        return countedRefers

    def date_filter(self, tweets):
        filtered_tweets = []
        date1 = re.findall('\d{1,2}/\d{1,2}/\d{4}', self.view.sDate.get())
        date2 = re.findall('\d{1,2}/\d{1,2}/\d{4}', self.view.eDate.get())
        if not date1:
            date1 = datetime(1970,1,1)
        else:
            date1 = date1[0]
            month, day, year = date1.split('/')
            date1 = datetime(int(year), int(month), int(day))
        if not date2:
            date2 = date2 = datetime.now()
        else:
            date2=date2[0]
            month, day, year = date2.split('/')
            date2 = datetime(int(year), int(month), int(day), 23, 59, 59)
        for tweet in tweets:
            tweet_date = datetime.strptime(tweet[2], '%Y-%m-%d %H:%M:%S')
            if date1 <= tweet_date <= date2:
                filtered_tweets.append(tweet)
        return filtered_tweets
                
    #call twitter stuff
