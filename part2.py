# This is part 2 of assignmnet 1 of Human computer interaction
# The goal of this part is to show the comments section of a post
# Made by Timo Strijbis

import tkinter as tk
from tkinter import *
from functools import partial
import praw
from tkinter import Menu

class commentTreeDisplay(tk.Frame):
    def __init__(self, parent):
        """Creating a frame first"""
        tk.Frame.__init__(self, parent)
        self.topframe = tk.Frame(self)
        self.text= tk.Text(self.topframe)
        

        """Creating a menubar"""
        menubar = Menu(self)
        self.master.config(menu=menubar)
        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="Exit", command=self.quit)
        menu_process = Menu(menubar, tearoff=0)
        menu_process.add_command(label="URL", command = self.URL_getter)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_process, label='Process')
        
        """Making a scrollbar and a texterea"""
        self.vsb= tk.Scrollbar(self.topframe, orient="vertical",command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.topframe.pack()

        

    def showComments(self):
        reddit = praw.Reddit(client_id='c1yvNSnNWly4Vw', client_secret = 'ECRVW8UyW8IikP3o6xF_ojut120HoQ', user_agent = 'assignment1')
        
        URL = self.E1.get()
        submission = reddit.submission(url=URL) 
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comment_no_emoji = comment.body.encode('ascii','ignore').decode()
            self.text.insert(tk.END, comment_no_emoji)
            
    def URL_getter(self):
        newframe = tk.Toplevel(self)
        L1 = tk.Label(newframe, text="Insert Reddit URL here: ")
        L1.pack(side="left")
        self.E1 = tk.Entry(newframe, bd =5)
        self.E1.pack(side="left")
        B1 = tk.Button(newframe, text="Show comments", command=self.showComments)
        B1.pack(side="right")


def main():
    submission_id = 'kgfdbc'
    root = Tk()
    root.title("Comments")


    st = commentTreeDisplay(root)
    st.pack()
    root.mainloop()
    
main()
