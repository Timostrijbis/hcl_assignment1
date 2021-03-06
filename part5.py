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


#from part1 import Data as data
#from part1 import Button as button
# from part2 import commentTreeDisplay

class Notebook(tk.Frame):

    def __init__(self, root, data, button):
        tk.Frame.__init__(self, root)
        self.root = root
        self.startGUI()
        self.reddit = praw.Reddit(client_id='QsDn3NogZO65jg',
                                  client_secret='BM2qzMdnQODzGW054E_WtwTF-94Zvg',
                                  user_agent='ChangeMeClient/0.1 by s2891131',
                                  username='s2891131',
                                  password='s28911311')
        self.data = data
        self.button = button

    def startGUI(self):
        self.root.title("part 5")

        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.master.config(menu=menubar)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Exit", command=self.quit)
        menu_process = tk.Menu(menubar, tearoff=0)
        menu_process.add_command(label="URL", command=self.URL_getter)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_process, label='Process')

        # This is where the frame is created, and divided into two pieces: Titles and comments
        self.topframe = tk.Frame(self.root)
        self.titleframe = tk.Frame(self.topframe)

        # From here you can initialize functions for the titleframe
        # Configuring root object
        self.titleframe.grid_columnconfigure(0, weight=0)
        self.titleframe.grid_columnconfigure(1, weight=0)
        self.titleframe.grid_columnconfigure(3, weight=1)
        self.pause_button = tk.Button(self.titleframe, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1)
        self.resume_button = tk.Button(self.titleframe, text="Resume", command=self.resume)
        self.resume_button.grid(row=0, column=2)
        self.exit_button = tk.Button(self.titleframe, text="Close", command=self.exitProgram)
        self.exit_button.grid(row=2, column=2)

        self.titleframe.after(1, self.updateGUI)
        self.displayStatus("Streaming most recent submissions")
        self.showList("")
        self.scaleBar1()


        # Set the treeview
        self.tree = ttk.Treeview(self.titleframe, columns=('Name'))

        # Set the heading (Attribute Names)
        self.tree.heading('#0', text='Submission title')
        self.tree.heading('#1', text='Subreddit name')

        self.tree.grid(row=5, columnspan=4, sticky='nsew')
        self.treeview1 = self.tree

        #Define modify black/whitelist button
        self.tosswl_button = tk.Button(self.titleframe, text="Clear whitelist", command=self.clearW)
        self.tossbl_button = tk.Button(self.titleframe, text= "Clear blacklist", command=self.clearB)

        # Define checkboxes for either black-or whitelist
        self.varwl = tk.IntVar()
        self.varbl = tk.IntVar()
        self.c1 = tk.Checkbutton(self.titleframe, text='Add to whitelist', variable=self.varwl, onvalue=1, offvalue=0, command=self.readCheckboxes)
        self.c1.grid(row=1, column=0)
        self.c2 = tk.Checkbutton(self.titleframe, text='Add to blacklist', variable=self.varbl, onvalue=1, offvalue=0, command=self.readCheckboxes)
        self.c2.grid(row=1, column=1)

        # This is the stuff for the commentframe, you don't need to do anything with this
        self.commentframe = tk.Frame(self.topframe)

        self.n = ttk.Notebook(self.commentframe)
        self.n.pack()
        self.treeview = self.tree
        self.iid = 0
        self.treeview.bind('<Double-1>', self.get_title_tab)
        self.URL = 'test'

        self.titleframe.pack(side=tk.LEFT)
        self.commentframe.pack(side=tk.RIGHT)
        self.topframe.pack()

        #/////// part1 functions ///////
    def clearW(self):
        self.tosswl_button.grid_forget()
        self.data.displaylist = ""
        self.data.whitelist = []
        self.showList("Whitelist cleared")

    def clearB(self):
        self.tossbl_button.grid_forget()
        self.data.displaylist = ""
        self.data.blacklist = []
        self.showList("Blacklist cleared")

    def pause(self):
        self.displayStatus("PAUSED, press 'resume' to continue")
        self.button.pauseButton()

    def resume(self):
        self.displayStatus("Streaming")
        self.button.resumeButton()
        self.data.startGettingData()

    # Exit behaviour
    def exitProgram(self):
        os._exit(1)


        # Checkboxes for adding white or blacklist
    def readCheckboxes(self):
        if self.varwl.get() == 1:
            self.c2.grid_forget()
            self.c1.grid_forget()
            self.input = tk.Entry(self.titleframe)
            self.input.grid(row=1, column=0)
            self.buttonwl = tk.Button(self.titleframe,text="Show this subreddit", command=self.getInputclearScreen)
            self.buttonwl.grid(row=1, column=1)
            self.showList("Add a subreddit to your whitelist")

        elif self.varbl.get() == 1:
            # self.l.config(text='Exclude a subreddit')
            self.input = tk.Entry(self.titleframe)
            self.input.grid(row=1, column=0)
            self.buttonbl = tk.Button(self.titleframe, text="Don't show this subreddit", command=self.getInputclearScreen)
            self.buttonbl.grid(row=1, column=1)
            self.c1.grid_forget()
            self.c2.grid_forget()

    # Clear screen after input for either white or blacklist is received
    def getInputclearScreen(self):
        userinput = self.input.get()
        if self.varwl.get() == 1 and self.data.sub_exists(userinput):
            self.data.appendtoWL(userinput)
            self.pause_button.grid_forget()
            self.resume_button.grid_forget()
            self.showList("Whitelisted: " + self.data.displaylist)
            self.tosswl_button.grid(row=1, column=3)
            self.input.delete(0, "end")
        elif self.varbl.get() == 1 and self.data.sub_exists(userinput):
            self.data.appendtoBL(userinput)
            self.showList("Excluded: " + self.data.displaylist)
            self.tossbl_button.grid(row=1, column=3)
            self.input.delete(0, "end")
        elif not self.data.sub_exists(userinput):
            self.input.delete(0, "end")
            self.showList("Subreddit does not exist!! Try again")

    # Top left blue bar displays updates when called
    def displayStatus(self, status):
        self.status = status
        self.label = tk.Label(self.titleframe, fg="white", bg="blue", text=self.status, width=30, height=2)
        self.label.grid(row=0, column=0)

    def showList(self, list):
        self.list = list
        self.label = tk.Label(self.titleframe, fg="white", bg="red", text=self.list, width=50, height=2)
        self.label.grid(row=0, column=3)

    def scaleBar1(self):
        self.scale = tk.Scale(self.titleframe, orient="horizontal", resolution=1,
                              from_=1, to=3, showvalue=0, command=self.setScaleStatus1)
        self.scale.grid(row=2, column=1)
        self.scale_label = tk.Label(self.titleframe, text="Streaming speed: >   >>   >>>")
        self.scale_label.grid(row=3, column=0)

    # Pass on Scalebar speed to Data class
    def setScaleStatus1(self, val):
        self.data.scaleBarStatus1(val)

    # Get data from queue for updating, process[0] is sub. title, process[1] is subreddit, process[2] is sub. id
    def updateGUI(self):
        try:
            process = self.data.shareQueue().get(block=False)
            if process is not None:
                self.treeview1.insert('', '0', iid=process[2], text=process[0], values=(process[1]))
        except queue.Empty:
            pass
        self.titleframe.after(1, self.updateGUI)

    def URL_getter(self):
        newframe = tk.Toplevel(self)
        self.L1 = tk.Label(newframe, text="Insert Reddit URL here: ")
        self.L1.pack(side="left")
        self.E1 = tk.Entry(newframe, bd=5)
        self.E1.pack(side="left")
        self.B1 = tk.Button(newframe, text="Show comments", command=self.make_new_tab)
        self.B1.pack(side="right")

    def make_new_tab(self):
        self.URL = self.E1.get()
        self.submission = self.reddit.submission(url=self.URL)
        self.submission.comments.replace_more(limit=None)
        self.frame = ttk.Frame(self.n)
        if len(self.submission.title) > 15:
            self.submission.title = self.submission.title[0:12]+ "..."
        self.n.add(self.frame, text = self.submission.title)
        self.newtree = ttk.Treeview(self.frame, columns=('Name'))
        self.newtree.grid(row=5, columnspan=1, sticky='nsew')
        self.newtreeview = self.newtree
        self.newiid = 0
        self.newtreeview.bind('<Double-1>', self.clicked)
        self.showComments2()

    def showComments2(self):
        for comment in self.submission.comments.list():
            comment_no_emoji = comment.body.encode('ascii','ignore').decode()
            self.newtreeview.insert('', '0', iid=comment.id, text=comment.id, values=([comment_no_emoji]))
        x = threading.Thread(target=self.comment_update, daemon=True)
        x.start()



    def get_title_tab(self, event):
        new_url = "https://www.reddit.com/r/memes/comments/lz7ral/jr_of_jars/"
        self.make_new_tab_2(new_url)


    def make_new_tab_2(self, new_url):
        self.URL = new_url
        self.submission = self.reddit.submission(url=self.URL)
        self.submission.comments.replace_more(limit=None)
        self.frame = ttk.Frame(self.n)
        if len(self.submission.title) > 15:
            self.submission.title = self.submission.title[0:12]+ "..."
        self.n.add(self.frame, text = self.submission.title)
        self.newtree = ttk.Treeview(self.frame, columns=('Name'))
        self.newtree.grid(row=5, columnspan=1, sticky='nsew')
        self.newtreeview = self.newtree
        self.newiid = 0
        self.showComments2()


    def scaleBar(self):
        self.scale = tk.Scale(self.commentframe, orient="horizontal", resolution=1,
                              from_=1, to=3, showvalue=0, command=self.scaleBarStatus)
        self.scale.pack()
        self.scale_label = tk.Label(self.commentframe, text="Refresh speed: 10sec   20sec   1min")
        self.scale_label.pack()


    def scaleBarStatus(self):
        self.status = self.scale.get()
        return self.status





class Data:

    # User data for Reddit
    def __init__(self, button):
        self.myqueue = queue.Queue()
        self.reddit = praw.Reddit(client_id='QsDn3NogZO65jg',
                                  client_secret='BM2qzMdnQODzGW054E_WtwTF-94Zvg',
                                  user_agent='ChangeMeClient/0.1 by s2891131',
                                  username='s2891131',
                                  password='s28911311')
        self.whitelist = []
        self.blacklist = []
        self.button = button
        self.displaylist = ""
        self.scaleSpeed = 1

    # Check if subreddit entered exists and return
    def sub_exists(self, sub):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
        return exists

    # Start thread and check for conditions to start with
    def startGettingData(self):
        threading.Thread(target=self.whiteAndblackList).start()

    # Define behavior in case of a whitelist item
    def appendtoWL(self,input):
        self.whitelist.append(input.lower())
        self.displaylist = self.displaylist+ input +", "

    def clearWL(self):
        self.whitelist = []
        print(self.whitelist)

    # Define behaviour in case of a blacklist item
    def appendtoBL(self,input):
        self.blacklist.append(input)
        self.button.blacklistButtonOn()
        self.displaylist = self.displaylist+ input +", "

    # Checks conditions in which to stream in
    def whiteAndblackList(self):
        if self.blacklist:
            total = "all"
            for item in self.blacklist:
                total = total+"-"+item
            threading.Thread(target=self.getData, args=(total,)).start()
        elif not self.blacklist:
            threading.Thread(target=self.getData, args=('all',)).start()

    # provide queue to class App
    def shareQueue(self):
        return self.myqueue

    # Get scalebar speed into Data class
    def scaleBarStatus1(self,var):
        self.scaleSpeed = var

    def checkSpeed(self):
        if self.scaleSpeed == "1":
            time.sleep(0.5)
        elif self.scaleSpeed == "2":
            time.sleep(0.2)
        elif self.scaleSpeed == "3":
            time.sleep(0.1)

    #process Reddit submissions
    def getData(self,item):
        for submission in self.reddit.subreddit(item).stream.submissions(skip_existing=True):
            if self.button.pressed:
                break
            if self.button.blacklistPressed:
                self.button.blacklistButtonOff()
                self.whiteAndblackList()
                break
            title = submission.title.encode('ascii','ignore').decode()
            subreddit = submission.subreddit.display_name.lower()
            if self.whitelist:
                if subreddit in self.whitelist:
                    self.myqueue.put((title, "/" + submission.subreddit.display_name, submission.id))
                    self.checkSpeed()
                else:
                    pass
            else:
                self.myqueue.put((title, "/" + submission.subreddit.display_name, submission.id))
                self.checkSpeed()

class Button:
    def __init__(self):
        self.pressed = False
        self.blacklistPressed = False

    def pauseButton(self):
        self.pressed = True

    def resumeButton(self):
        self.pressed = False

    def blacklistButtonOn(self):
        self.blacklistPressed=True

    def blacklistButtonOff(self):
        self.blacklistPressed=False

def main():
    button = Button()
    data = Data(button)
    start = Notebook(tk.Tk(), data, button)
    data.startGettingData()
    start.mainloop()


if __name__ == "__main__":
    main()