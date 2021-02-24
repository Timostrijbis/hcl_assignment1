import tkinter as tk
from tkinter import *
from functools import partial
import praw
from tkinter import Menu
import threading
from tkinter import simpledialog
from part2 import commentTreeDisplay


class ResponseCommentTreeDisplay(commentTreeDisplay):

    def __init__(self, parent):
        commentTreeDisplay.__init__(self,parent)
    # Creating event
        self.treeview.bind('<Double-1>', self.clicked)

    def clicked(self,event):
        tv = self.treeview
        self.promptcomment = tv.item(tv.selection())['values'][0]
        print(tv.selection())
        self.comment()


    def comment(self):
        newframe2 = tk.Toplevel(self)
        l2 = tk.Label(newframe2, text="Respond to this comment:")
        l2.pack()
        comment_prompt = simpledialog.askstring(title = "Comment prompt", prompt = "Comment to: /////" +self.promptcomment+ "///// ")
        if comment_prompt:
            print("You commented: "+comment_prompt)

        elif not comment_prompt:
            again = simpledialog.askstring(title = "Comment to this", prompt = "Cannot be empty")
            if again:
                print("You commented: "+again)



def main():
    submission_id = 'kgfdbc'
    root = Tk()
    root.title("Comments")

    rt = ResponseCommentTreeDisplay(root)
    rt.pack()
    root.mainloop()

main()