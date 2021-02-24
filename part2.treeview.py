import tkinter as tk
from tkinter import *
from functools import partial
import praw
from tkinter import Menu
import tkinter.ttk as ttk

class commentTreeDisplay(tk.Frame):
    def __init__(self, parent):
        """Creating a frame first"""
        tk.Frame.__init__(self, parent)
        self.topframe = tk.Frame(self)
        self.text = tk.Text(self.topframe)
        self.reddit = praw.Reddit(client_id='c1yvNSnNWly4Vw', client_secret='ECRVW8UyW8IikP3o6xF_ojut120HoQ',
                             user_agent='assignment1')



        """Creating a menubar"""
        menubar = Menu(self)
        self.master.config(menu=menubar)
        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="Exit", command=self.quit)
        menu_process = Menu(menubar, tearoff=0)
        menu_process.add_command(label="URL", command=self.URL_getter)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_process, label='Process')

        """Making a scrollbar and a texterea"""
        # Set the treeview
        self.tree = ttk.Treeview(self, columns=('Name'))

        # Set the heading (Attribute Names)


        self.tree.grid(row=5, columnspan=1, sticky='nsew')
        self.treeview = self.tree
        self.iid = 0

        #self.vsb = tk.Scrollbar(self.topframe, orient="vertical", command=self.text.yview)
        #self.text.configure(yscrollcommand=self.vsb.set)
        #self.vsb.pack(side="right", fill="y")
        #self.text.pack(side="left", fill="both", expand=True)
        #self.topframe.pack()

    def showComments(self):
        URL = self.E1.get()
        submission = self.reddit.submission(url=URL)
        submission.comments.replace_more(limit=None)
        self.iid = 1
        for comment in submission.comments.list():
            self.treeview.insert('', '0', iid=self.iid, text="comment #"+str(self.iid), values=([comment.body]))
            self.iid = self.iid + 1

    def URL_getter(self):
        newframe = tk.Toplevel(self)
        L1 = tk.Label(newframe, text="Insert Reddit URL here: ")
        L1.pack(side="left")
        self.E1 = tk.Entry(newframe, bd=5)
        self.E1.pack(side="left")
        B1 = tk.Button(newframe, text="Show comments", command=self.showComments)
        B1.pack(side="right")
