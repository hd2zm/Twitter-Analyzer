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

        searchUsername = Button(self.parent, text="     Search     ", command = self.govnah.searchUsername)
        searchUsername.grid(row = 2, column =0, columnspan = 3)

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

    def chngPath(self):
        self.path = self.pathEntry.get()
        self.govnah.changeDir(self.path)

    def valid(self, d, i, P, s, S, v, V, W):
        if not self.lock:
            self.uname = P
            if self.govnah.userExists(P):
                self.goodMessage("Valid User")
            else:
                self.badMessage("User not Found")
        return not self.lock

    def goodMessage(self, msg):
        self.uinfo.config(text=msg, fg="forest green")

    def badMessage(self, msg):
        self.uinfo.config(text=msg, fg="red")

    def alert(self):
        top = Toplevel()
        top.title("Are you sure?")

        msg = Message(top, text="Are you sure?")
        msg.pack()

        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()

        self.center(top)

    def areYouSureDelete(self):
        return tkMessageBox.askyesno("Confirmation", "Are you sure you want delete " + self.uname)

    def delUser(self):
        if self.govnah.userExists(self.uname):
            self.lock = True
            if self.areYouSureDelete():
                self.govnah.delUser(str(self.uname))
                self.appendText("User: " + self.uname + " successfully deleted.")
                self.appendText("")
            self.lock = False


    def appendText(self, text):
        self.log.insert(END, str(text.encode("utf-8")) + "\n")
        self.log.see(END)

    def getNewPw(self):
        if self.govnah.userExists(self.uname):
            self.unameforpwch = self.uname
            self.lock = True
            self.top = Toplevel()
            self.top.protocol('WM_DELETE_WINDOW', self.closePwWindow)
            self.top.title = "Change Password"
            l = Label(self.top, text="Enter a new Password for user: " + self.unameforpwch)
            l.grid(row=0, columnspan=2)
            self.entry = Entry(self.top, width=20, bg="white")
            self.entry.grid(row=1, columnspan=2)
            n = Button(self.top, text="Cancel", command=self.closePwWindow)
            n.grid(row=2, column=0)
            y = Button(self.top, text="Proceed", command=self.confirmPwChange)
            y.grid(row=2, column=1)
            self.center(self.top)

    def closePwWindow(self):
        self.lock = False
        self.top.destroy()
        self.appendText("Password for " + self.unameforpwch + " not changed")
        self.appendText("")

    def confirmPwChange(self):
        pw = self.entry.get()
        if len(pw) > 0:
            self.govnah.chUserPass(self.unameforpwch, pw)
            self.top.destroy()
            self.appendText("Password for " + self.unameforpwch + " successfully changed to " + pw)
            self.appendText("")
            self.lock = False

    def center(self, win):
        win.withdraw()
        win.update_idletasks()  # Update "requested size" from geometry manager

        x = (win.winfo_screenwidth() - self.parent.winfo_reqwidth()) / 2
        y = (win.winfo_screenheight() - self.parent.winfo_reqheight()) / 2
        win.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        win.deiconify()

# This module implements a MVC model. This class is the View and contains the UI Stuff
