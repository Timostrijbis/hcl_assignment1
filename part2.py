import tkinter as tk
from tkinter import *
from functools import partial
import praw
from tkinter import Menu
import tkinter.ttk as ttk

class commentTreeDisplay(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Creating a frame first"""
        tk.Frame.__init__(self, parent)
        self.topframe = tk.Frame(self)
        self.text = tk.Text(self.topframe)
        self.reddit = praw.Reddit(client_id='QsDn3NogZO65jg',
                                  client_secret='BM2qzMdnQODzGW054E_WtwTF-94Zvg',
                                  user_agent='ChangeMeClient/0.1 by s2891131',
                                  username='s2891131',
                                  password='s28911311')

        """Creating a menubar"""
        menubar = Menu(self)
        self.master.config(menu=menubar)
        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="Exit", command=self.quit)
        menu_process = Menu(menubar, tearoff=0)
        menu_process.add_command(label="URL", command=self.URL_getter)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_process, label='Process')

        """Making a scrollbar and a textarea"""
        # Set the treeview
        self.tree = ttk.Treeview(self, columns=('Name'))

        # Set the heading (Attribute Names)

        self.tree.grid(row=5, columnspan=1, sticky='nsew')
        self.treeview = self.tree
        self.iid = 0
        self.URL = 'test'


    def showComments(self):
        self.URL = self.E1.get()
        self.submission = self.reddit.submission(url=self.URL)
        self.submission.comments.replace_more(limit=None)
        for comment in self.submission.comments.list():
            comment_no_emoji = comment.body.encode('ascii','ignore').decode()
            self.treeview.insert('', '0', iid=comment.id, text=comment.id, values=([comment_no_emoji]))
            

    def URL_getter(self):
        newframe = tk.Toplevel(self)
        L1 = tk.Label(newframe, text="Insert Reddit URL here: ")
        L1.pack(side="left")
        self.E1 = tk.Entry(newframe, bd=5)
        self.E1.pack(side="left")
        B1 = tk.Button(newframe, text="Show comments", command=self.showComments)
        B1.pack(side="right")
