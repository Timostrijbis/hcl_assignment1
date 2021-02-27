import tkinter as tk
from tkinter import *
from functools import partial
import praw
from tkinter import Menu
import threading
from tkinter import simpledialog
from part2 import commentTreeDisplay
import time

class UpdatedTreeDisplay(commentTreeDisplay):
    def __init__(self, parent, *args, **wkargs):
        commentTreeDisplay.__init__(self,parent)
        self.scaleBar()
    
    # Scalebar for adjusting streaming speed
    def scaleBar(self):
        self.scale = tk.Scale(self, orient="horizontal", resolution=1,
                        from_=1, to=3, showvalue=0)
        self.scale.grid(row=3, column=0)
        self.scale_label = tk.Label(self, text="Refresh speed: 10sec   20sec   1min")
        self.scale_label.grid(row=2, column=0)
        
    # Return status of scale
    def scaleBarStatus(self):
        self.status = self.scale.get()
        return self.status        

    # Checks for new comment, updates treeview if there are any, then sleeps for a time selected in the scalebar        
    def comment_update(self):
        while True:
            # If there is no reddit URL given, this function does nothing
            if self.URL == 'test':
                pass
            # Once a reddit URL is given, it checks for new comments
            else:
                new_comments = ''
                self.submission = self.reddit.submission(url=self.URL)
                self.submission.comments.replace_more(limit=None)
                for comment in self.submission.comments.list():
                    if comment in self.tree.get_children():
                        pass
                    else:
                        new_comments = comment
                # If there are new comments, the treeview gets updated, by deleting old comments and running showComments()
                if new_comments != '':
                    self.tree.delete(*self.tree.get_children())
                    commentTreeDisplay.showComments(self)
                        
                if self.scaleBarStatus() == 1:
                    time.sleep(10)
                elif self.scaleBarStatus() == 2:
                    time.sleep(20)
                elif self.scaleBarStatus() == 3:
                    time.sleep(60)
     
        
def main():

    root = Tk()
    root.title("Comments")
    rt = UpdatedTreeDisplay(root)
    x = threading.Thread(target=rt.comment_update, daemon=True)
    x.start()

    rt.pack()
    root.mainloop()

main()
