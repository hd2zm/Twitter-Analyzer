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
from twitter_interface import *
from twitter_reader import *
from twitter_db_ops import *

# The main class for this module. This class is the controller and defines the behaviours.
class SInterface():

    def __init__(self):
        # This is the model. The db class is a wrapper around database operations.
        self.dbops = TwitterDbOps("")
        self.root =Tk()
        self.root.geometry("1150x400+100+100")

        self.consumerKey = 'jf1RuBnCqdQCNmLX0frLg'
        self.consumerSecret = 'ThqOiemmb6u0unxovHEg9r9m4Lf0MaI30nqh3gwedI'
        self.accessKey = '1106939719-KyTHxcGncJp0vgxTjH8P2AmaGQ13B5ert7YZR0t'
        self.accessSecret = 'PqIuAYKTuKFfrg24CAhuwigh5R2udkl2Fls06mTaZLhXZ'
        self.tweetReader = TwitterReader(self.consumerKey,self.consumerSecret,self.accessKey,self.accessSecret)

        #img = ImageTk.PhotoImage(file='img/logo50.png')
        #self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        self.view = View(self.root, self)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def menu(self):
        print "Howdy Admin! Please select an option:"
        print "-----------------------------------------"
        print "1. Print OneDir Users by Username"
        print "2. Print OneDir Users by Registration Time"
        print "3. Print Recent Transactions"
        print "4. Delete a User"
        print "5. Change a user's password"
        print "6. Start Server Daemon"
        print "0. Exit"
        print "-----------------------------------------\n"
    '''
    def printUsersByName(self):
        self.view.appendText("The list of users, sorted by username. (Unique ID, username, password hash, registration timestamp)")
        self.printSanitizeDBstr(self.db.getUsersByUName())
    '''
    def verifyUsername(self):
        self.valid = False
        if self.tweetReader.lookup_user(self.view.username.get()):
            self.view.username.config(bg='green')
            self.view.appendText("User: %s is valid!" %self.view.username.get())
            self.valid = True
        else:
            self.view.username.config(bg='red')

    def searchUsername(self):
        try:
            if self.valid:
                try:
                    tweets=self.tweetReader.get_tweets_from_user(self.view.username.get(),int(self.view.numTweets.get()))
                    self.tweetsToDB(tweets)
                    #self.view.appendText(str(len(tweets)))
                except TwitterReaderException:
                    self.view.appendText("Rate Limit Exceeded; Please wait 15 minutes.")
        except AttributeError:
            self.view.appendText("Please enter and verify a user.")

    def listTweets(self):
        #print self.view.numTweets.get()
        if self.view.numTweets.get() == "":
            tweets = self.dbops.getTweetsForList(self.view.numTweets.get(),False)
        else:
            tweets = self.dbops.getTweetsForList(self.view.numTweets.get(),True)
        for tweet in tweets:
            self.view.appendText(tweet[2])
            self.view.appendText(tweet[1] + "\n")

    def mostHash(self):
        hashes = self.dbops.getHashtags()
        hashdict = {}
        hasharray = []

        for hash in hashes:
            if hash[0].lower() in hashdict:
                hashdict[hash[0].lower()]= hashdict[hash[0].lower()]+1
            else:
                hashdict[hash[0].lower()] = 1
        for n in hashdict:
            hasharray.append((hashdict[n],n))
        hasharray.sort(reverse=True)
        self.view.appendText("Most used Hashtags:")
        #print hasharray
        #print hashdict
        for n in hasharray:
            self.view.appendText('%s used %d times'%(n[1],n[0]))
        self.view.appendText('\n')

    def timeGraph(self):
        pass

    def communicated(self):
        refers = self.dbops.getReferences()
        refdict = {}
        refarray = []

        for refer in refers:
            if refer[0].lower() in refdict:
                refdict[refer[0].lower()]= refdict[refer[0].lower()]+1
            else:
                refdict[refer[0].lower()] = 1
        for n in refdict:
            refarray.append((refdict[n],n))
        refarray.sort(reverse=True)
        self.view.appendText("Most used References:")
        #print refarray
        #print refdict
        for n in refarray:
            self.view.appendText('%s used %d times'%(n[1],n[0]))
        self.view.appendText('\n')

    def tweetsToDB(self,tweets):
        for tweet in tweets:
            self.dbops.createTweet(tweet['text'], self.tweetReader.parse_date(tweet['created_at']))
    #call twitter stuff
    #def printUsersFileSpace(self):
    #    users = self.db.getUsersByUName()
    #    for row in users:
    #        up = os.path.join(self.path, row[1])
    #        try:
    #            self.view.appendText(row[1] + " " + str(common.get_size(up)/1024) + "KB")
    #        except:
    #            pass

    #def printTotalFileSpace(self):
    #    up = os.path.join(self.path)
    #    self.view.appendText("Total file space used by all users: " + str(common.get_size(up)/1024) + "KB")

    def printSanitizeDBstr(self, results):
        for entry in results:
            t = ""
            for item in entry:
                t = t + str(item) + "\t"
            self.view.appendText(t)
        self.view.appendText("")

    def printSanitizeDBstrDub(self, results):
        for entry in results:
            t = ""
            for item in entry:
                t = t + str(item) + "\t\t"
            self.view.appendText(t)
        self.view.appendText("")

    def userExists(self, userName):
        return self.db.userExists(userName)

    def delUser(self, userName):
        if self.db.userExists(userName):
            self.db.deleteUser(userName)

    def chUserPass(self, usr, pw):
        if self.db.userExists(usr):
            self.db.updatePassword(usr, pw)

    def setOption(self, option, value):
        if self.prefs.optionExists(option):
            self.prefs.setOption(option, value)

    def start(self):
        while True:
            self.menu()
            x = int(raw_input('What would you like to do? '))
            if not (x >= 1 or x <= 6):
                print "Invalid Option \n\n"
                continue
            elif x == 0:
                print "Interface Exit"
                break
            elif x == 1:
                for u in self.db.getUsersByUName():
                    print u
            elif x == 2:
                for u in self.db.getUsersByTime():
                    print u
            elif x == 3:
                print "Not yet implemented"
            elif x == 4:
                str = raw_input("Which user name?")
                if self.db.userExists(str):
                    self.db.deleteUser(str)
                else:
                    print "That user does not exist."
            elif x == 5:
                str = raw_input("Which user name?")
                if self.db.userExists(str):
                    pw = raw_input("Enter the new password: ")
                    self.db.updatePassword(str, pw)
                else:
                    print "That user does not exist.\n\n"
