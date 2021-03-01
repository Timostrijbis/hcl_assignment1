#part1.py
#This program displays a stream of newly posted submissions
#Priscilla Postma s2891131

import tkinter as tk; import tkinter.ttk as ttk;import requests;import praw;
import threading;import queue;import time; from prawcore import NotFound;import os

class Application(tk.Frame):

    def __init__(self, root, data, button):
        self.data = data
        self.button = button
        self.root = root
        self.initializeGUI()
        self.root.after(1, self.updateGUI)
        self.displayStatus("Streaming most recent submissions")
        self.scaleBar()
        self.reddit = praw.Reddit(client_id='QsDn3NogZO65jg',
                                  client_secret='BM2qzMdnQODzGW054E_WtwTF-94Zvg',
                                  user_agent='ChangeMeClient/0.1 by s2891131',
                                  username='s2891131',
                                  password='s28911311')

    def initializeGUI(self):
        # Configuring root object
        self.root.title("Incoming submissions")
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.geometry("800x290")

        # Define pause & resume button
        self.pause_button = tk.Button(self.root, text="Pause", command=self.button.pauseButton)
        self.pause_button.grid(row=0, column=1)
        self.resume_button = tk.Button(self.root, text="Resume", command=self.button.resumeButton)
        self.resume_button.grid(row=0, column=2)
        self.exit_button = tk.Button(self.root, text="Close", command=self.exitProgram)
        self.exit_button.grid(row=2, column=2)

        # Define checkboxes for either black-or whitelist
        self.varwl = tk.IntVar()
        self.varbl = tk.IntVar()
        self.c1 = tk.Checkbutton(self.root, text='Add to whitelist', variable=self.varwl, onvalue=1, offvalue=0, command=self.readCheckboxes)
        self.c1.grid(row=1, column=0)
        self.c2 = tk.Checkbutton(self.root, text='Add to blacklist', variable=self.varbl, onvalue=1, offvalue=0, command=self.readCheckboxes)
        self.c2.grid(row=1, column=1)

        # Set the treeview
        self.tree = ttk.Treeview(self.root, columns=('Name'))

        # Set the heading (Attribute Names)
        self.tree.heading('#0', text='Submission title')
        self.tree.heading('#1', text='Subreddit name')

        self.tree.grid(row=5, columnspan=4, sticky='nsew')
        self.treeview = self.tree

    # Exit behaviour
    def exitProgram(self):
        os._exit(1)

    # Checkboxes for adding white or blacklist
    def readCheckboxes(self):
        self.l = tk.Label(self.root, bg='white', width=30, text='')
        self.l.grid(row=0, column=3)
        if self.varwl.get() == 1:
            self.l.config(text='Add a subreddit to your whitelist')
            self.input = tk.Entry(self.root)
            self.input.grid(row=1, column=3)
            self.buttonwl = tk.Button(text="Show this subreddit", command=self.getInputclearScreen)
            self.buttonwl.grid(row=2,column=3)
            self.c2.grid_forget()
            
        elif self.varbl.get() == 1:
            self.l.config(text='Exclude a subreddit')
            self.input = tk.Entry(self.root)
            self.input.grid(row=1, column=3)
            self.buttonbl = tk.Button(text="Don't show this subreddit", command=self.getInputclearScreen)
            self.buttonbl.grid(row=2, column=3)
            self.c1.grid_forget()


    # Clear screen after input for either white or blacklist is received
    def getInputclearScreen(self):
        userinput = self.input.get()
        if self.varwl.get() == 1 and self.data.sub_exists(userinput):
            self.data.appendtoWL(userinput)
            self.pause_button.grid_forget()
            self.resume_button.grid_forget()
            self.displayStatus("Streaming '"+userinput+"' subreddit")
        elif self.varbl.get() == 1 and self.data.sub_exists(userinput):
            self.data.appendtoBL(userinput)
            self.displayStatus("Excluded '"+userinput+"'")

        elif not self.data.sub_exists(userinput):
            self.input.delete(0,"end")
            self.displayStatus("Subreddit does not exist!! Try again")

    # Top left blue bar displays updates when called
    def displayStatus(self,status):
        self.status = status
        self.label = tk.Label(self.root, fg="white", bg="blue", text=self.status,width=30, height=2)
        self.label.grid(row=0, column=0,padx=1, pady=1)

    # Scalebar for adjusting streaming speed
    def scaleBar(self):
        self.scale = tk.Scale(self.root, orient="horizontal", resolution=1,
                        from_=1, to=3, showvalue=0, command=self.setScaleStatus)
        self.scale.grid(row=2, column=1)
        self.scale_label = tk.Label(self.root, text="Streaming speed: >   >>   >>>")
        self.scale_label.grid(row=2, column=0)

    # Pass on Scalebar speed to Data class
    def setScaleStatus(self,val):
        self.data.scaleBarStatus(val)

    # Get data from queue for updating, process[0] is sub. title, process[1] is subreddit, process[2] is sub. id
    def updateGUI(self):
        try:
            process = self.data.shareQueue().get(block=False)
            if process is not None:
                self.treeview.insert('', '0', iid=process[2], text=process[0], values=(process[1]))
        except queue.Empty:
            pass
        self.root.after(1, self.updateGUI)

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
        print(self.whitelist)

    # Define behaviour in case of a blacklist item
    def appendtoBL(self,input):
        self.blacklist.append(input)
        self.button.blacklistButtonOn()

    # Checks conditions in which to stream in
    def whiteAndblackList(self):
        if self.blacklist:
            total = "all"
            for item in self.blacklist: #ingericht op meerdere items, start voor elke een thread
                total = total+"-"+item
            threading.Thread(target=self.getData, args=(total,)).start()
        elif not self.blacklist: #if there is no blacklist: stream all
            threading.Thread(target=self.getData, args=('all',)).start()

    # provide queue to class App
    def shareQueue(self):
        return self.myqueue

    # Get scalebar speed into Data class
    def scaleBarStatus(self,var):
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
            title = submission.title.encode('ascii','ignore').decode() #Emojis verwijderd vanwege vastlopen
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
        app.displayStatus("PAUSED, press 'resume' to continue")

    def resumeButton(self):
        data = Data()
        self.pressed = False
        app.displayStatus("Streaming")
        data.startGettingData()

    def blacklistButtonOn(self):
        self.blacklistPressed=True

    def blacklistButtonzOff(self):
        self.blacklistPressed=False

def main():
    button = Button()
    data = Data(button)
    app = Application(tk.Tk(), data, button)
    data.startGettingData()
    app.root.mainloop()

main()