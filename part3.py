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
        try:
            tv = self.treeview
            self.promptcomment = tv.item(tv.selection())['values'][0]
            self.commentid = tv.item(tv.selection())['text']
            self.comment()
        except IndexError:
            pass

    def comment(self):
        commenttorespondto = self.reddit.comment(id=self.commentid)
        comment_prompt = simpledialog.askstring(title="Comment prompt",
                                                prompt="Comment to: /////" + self.promptcomment + "///// ")
        if comment_prompt:
            commenttorespondto.reply(comment_prompt)

        elif not comment_prompt:
            comment_prompt = simpledialog.askstring(title="Comment to this", prompt="Field can't be empty, try again.")
            if comment_prompt:
                commenttorespondto.reply(comment_prompt)
            if not comment_prompt:
                pass


def main():
    root = Tk()
    root.title("Comments")

    rt = ResponseCommentTreeDisplay(root)
    rt.pack()
    root.mainloop()

main()