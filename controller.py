__author__ = 'owner'
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
import twitter_interface

# The main class for this module. This class is the controller and defines the behaviours.
class SInterface():

    def __init__(self):
        self.prefs = twitter_db_ops.ServerPrefs()
        self.path = self.prefs.getOption("path")
        # This is the model. The db class is a wrapper around database operations.
        self.db = twitter_db_ops.DbOps(self.path)
        self.dview = None
        self.dioq = Queue.Queue()
        self.dioeq = Queue.Queue()
        self.root =Tk()
        self.root.geometry("1150x400+100+100")
        #img = ImageTk.PhotoImage(file='img/logo50.png')
        #self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        self.view = twitter_interface.View(self.root, self)
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

    def printUsersByName(self):
        self.view.appendText("The list of users, sorted by username. (Unique ID, username, password hash, registration timestamp)")
        self.printSanitizeDBstr(self.db.getUsersByUName())

    def printUsersByTime(self):
        self.view.appendText("The list of users, sorted by registration time. (Unique ID, username, password hash, registration timestamp)")
        self.printSanitizeDBstr(self.db.getUsersByTime())

    def printTransByUser(self):
        self.view.appendText("The list of transactions, sorted by username. (Unique ID, username, type, path, size, timestamp)")
        self.printSanitizeDBstrDub(self.db.getTransByUser())

    def printTransBySize(self):
        self.view.appendText("The list of transactions, sorted by size. (Unique ID, username, type, path, size, timestamp)")
        self.printSanitizeDBstrDub(self.db.getTransBySize())

    def printTransByTime(self):
        self.view.appendText("The list of transactions, sorted by timestamp. (Unique ID, username, type, path, size, timestamp)")
        self.printSanitizeDBstrDub(self.db.getTransByTime())

    def printTransByType(self):
        self.view.appendText("The list of transactions, sorted by type. (Unique ID, username, type, path, size, timestamp)")
        self.printSanitizeDBstrDub(self.db.getTransByType())

    def searchUsername(self):
        pass
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

    def changeDir(self, path):
        self.prefs.checkPath(path)
        self.prefs.setOption("path", path)
        self.path = path
        self.db = twitter_db_ops.DbOps(self.path)
        if self.daemon is not None:
            self.view.appendText("OneDir Directory has changed to: " + self.path + " but there is still a daemon running on"
                                 + self.dview.path)
        else:
            self.view.appendText("One Directory has changed to: " + self.path)


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
