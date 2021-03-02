import tkinter as tk

import tkinter.ttk as ttk
import requests
import praw
import threading
import queue
import time
from prawcore import NotFound
from tkinter import simpledialog
import os
#from part1 import Application, Data, Button
#from part2 import commentTreeDisplay

class Notebook(tk.Frame):
    
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.startGUI()
        self.reddit = praw.Reddit(client_id='QsDn3NogZO65jg',
                                  client_secret='BM2qzMdnQODzGW054E_WtwTF-94Zvg',
                                  user_agent='ChangeMeClient/0.1 by s2891131',
                                  username='s2891131',
                                  password='s28911311')

    def startGUI(self):
        self.root.title("part 5")
        
        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.master.config(menu=menubar)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Exit", command=self.quit)
        menu_process = tk.Menu(menubar, tearoff=0)
        menu_process.add_command(label="URL", command = self.URL_getter)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_process, label='Process')
        
        # This is where the frame is created, and devided into two pieces: Titles and comments
        self.topframe = tk.Frame(self.root)
        self.titleframe = tk.Frame(self.topframe)
        
        
        
        
        
        
        
        
        
        #From here you can initialize functions for the titleframe
        self.title_label = tk.Label(self.titleframe, text = "put part1 here")
        self.title_label.pack()
        self.text = tk.Text(self.titleframe)
        self.text.pack()
        
        
        
        
        
        
        
        # This is the stuff for the commentframe, you don't need to do anything with this
        self.commentframe = tk.Frame(self.topframe)
        self.scaleBar()
        self.n = ttk.Notebook(self.commentframe)
        self.n.pack()
        self.f1 = ttk.Frame(self.n)
        self.n.add(self.f1, text = "Post titles")
        self.tree = ttk.Treeview(self.f1, columns=('Name'))
        self.tree.grid(row=5, columnspan=1, sticky='nsew')
        self.treeview = self.tree
        self.iid = 0
        self.treeview.bind('<Double-1>', self.clicked)
        self.URL = 'test'
        
        self.titleframe.pack(side = tk.LEFT)
        self.commentframe.pack(side = tk.RIGHT)
        self.topframe.pack()
        




        # Here is room for your functions






    def URL_getter(self):
        newframe = tk.Toplevel(self)
        self.L1 = tk.Label(newframe, text="Insert Reddit URL here: ")
        self.L1.pack(side="left")
        self.E1 = tk.Entry(newframe, bd=5)
        self.E1.pack(side="left")
        self.B1 = tk.Button(newframe, text="Show comments", command=self.showComments)
        self.B1.pack(side="right")
        
    def showComments(self):
        self.URL = self.E1.get()
        self.submission = self.reddit.submission(url=self.URL)
        self.submission.comments.replace_more(limit=None)
        for comment in self.submission.comments.list():
            comment_no_emoji = comment.body.encode('ascii','ignore').decode()
            self.treeview.insert('', '0', iid=comment.id, text=comment.id, values=([comment_no_emoji]))
            
    def clicked(self,event):
        tv = self.treeview
        self.promptcomment = tv.item(tv.selection())['values'][0]
        self.commentid = tv.item(tv.selection())['text']
        self.comment()
        
    def comment(self):
        commenttorespondto = self.reddit.comment(id=self.commentid)
        comment_prompt = simpledialog.askstring(title = "Comment prompt", prompt = "Comment to: /////" +self.promptcomment+ "///// ")
        if comment_prompt:
            commenttorespondto.reply(comment_prompt)
            print("You commented: "+comment_prompt)

        elif not comment_prompt:
            again = simpledialog.askstring(title = "Comment to this", prompt = "Cannot be empty")
            if again:
                print("You commented: "+again)
                
    def scaleBar(self):
        self.scale = tk.Scale(self.commentframe, orient="horizontal", resolution=1,
                        from_=1, to=3, showvalue=0)
        self.scale.pack()
        self.scale_label = tk.Label(self.commentframe, text="Refresh speed: 10sec   20sec   1min")
        self.scale_label.pack()
        
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
    start = Notebook(tk.Tk())
    x = threading.Thread(target=start.comment_update, daemon=True)
    x.start()
    start.mainloop()    
        
if __name__ == "__main__":
    main()



