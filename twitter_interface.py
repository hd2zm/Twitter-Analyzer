from Tkinter import *
from ttk import Frame, Style
import twitter_db_ops
from idlelib.WidgetRedirector import WidgetRedirector
import tkMessageBox
from PIL import ImageTk, Image
import subprocess
import threading
import Queue
import os

# A small class that wraps the TextView widgets so they are read only
class ReadOnlyText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
        self.delete = self.redirector.register("delete", lambda *args, **kw: "break")

# This module implements a MVC model. This class is the View and contains the UI Stuff
class View(Frame):
    def __init__(self, parent, govnah):# govnah = siinterface
        self.govnah = govnah
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.lock = False

    def initUI(self):
        self.parent.title("Twitter Interface")
        #self.pack(fill=BOTH, expand=1)
        commands = Label(self.parent, text="Commands")
        commands.grid(row=0, columnspan=3)
        output = Label(self.parent, text="Output")
        output.grid(row=0, column=3)

        scrollbar = Scrollbar(self.parent)
        scrollbar.grid(row=1, column=4, rowspan=100, sticky=N+S)

        self.log = ReadOnlyText(self.parent, bg="white", undo=False, yscrollcommand=scrollbar.set, width=120)
        self.log.grid(row=1, column=3, rowspan=100)

        scrollbar.config(command=self.log.yview)

        ulabel = Label(self.parent, text="Username: ")
        ulabel.grid(row=1, column=0)

        self.username = Entry(self.parent, width=14, bg="white")
        self.username.grid(row=1, column=1, columnspan=2)

        searchUsername = Button(self.parent, text="Verify User", command = self.govnah.verifyUsername)
        searchUsername.grid(row = 2, column =0, columnspan = 1)

        searchUsername = Button(self.parent, text="Get Tweets", command = self.govnah.searchUsername)
        searchUsername.grid(row = 2, column =2, columnspan = 1)

        ntlabel = Label(self.parent, text = "Number of Tweets:")
        ntlabel.grid(row = 3, column = 0)

        self.numTweets = Entry(self.parent, width = 14, bg = "white")
        self.numTweets.grid(row = 3, column = 2)
        self.numTweets.insert(END,"20")

        sdlabel = Label(self.parent, text = "Start Date:")
        sdlabel.grid(row = 4, column = 0)

        self.sDate = Entry(self.parent, width = 14, bg = "white")
        self.sDate.grid(row = 5, column = 0)
        self.sDate.insert(END,"MM/DD/YYYY")

        edlabel = Label(self.parent, text = "End Date:")
        edlabel.grid(row = 4, column = 2)

        self.eDate = Entry(self.parent, width = 14, bg = "white")
        self.eDate.grid(row = 5, column = 2)
        self.eDate.insert(END,"MM/DD/YYYY")

        searchUsername = Button(self.parent, text="List Tweets", command = self.govnah.listTweets, width = 20 )
        searchUsername.grid(row = 6, column =0, columnspan = 3)

        searchUsername = Button(self.parent, text="Most Used Hashtags", command = self.govnah.mostHash, width = 20 )
        searchUsername.grid(row = 7, column =0, columnspan = 3)

        searchUsername = Button(self.parent, text="Time graph", command = self.govnah.timeGraph, width = 20 )
        searchUsername.grid(row = 8, column =0, columnspan = 3)

        searchUsername = Button(self.parent, text="Most Communicated with", command = self.govnah.communicated, width = 20 )
        searchUsername.grid(row = 9, column =0, columnspan = 3 )

        original = Image.open("twitlogo.png")
        resized = original.resize((125, 125), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        logoLabel = Label(self.parent, image=self.img)
        logoLabel.grid(row=11, column=0, rowspan=3, columnspan=3)

        self.log.insert(END, "Welcome to the Twitter Analyzer! \n\n")

    def appendText(self, text):
        self.log.insert(END, str(text.encode("utf-8")) + "\n")
        self.log.see(END)