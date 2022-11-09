# login file
# allows the user to login to the server and save their score


from zeinahw7 import *
import tkinter
from tkinter import messagebox
class start():
    def __init__(self, win, comm):
        self.root = win
        self.root.geometry("300x200")
        self.frame = tkinter.Frame(self.root)
        self.frame.configure(bg= "#808080")
        self.frame.pack()
        self.username = tkinter.Label(self.root, text = "Username", font =( "Courier",20))
        self.username.pack(pady = 5)
        self.usernameBox = tkinter.Entry(win)
        self.usernameBox.pack(pady = 5)
        self.password = tkinter.Label(self.root, text = "Password", font = ("Courier",20))
        self.password.pack(pady = 5)
        self.passwordBox = tkinter.Entry(win, show = "*")
        self.passwordBox.pack(pady = 5)
        self.ok = tkinter.Button(self.root, text = "OK", command = self.login, pady = 5, padx= 40)
        self.ok.pack()
        self.user = None
        
    def login(self):
        user = self.usernameBox.get()
        passes = self.passwordBox.get()
        if not comm.login(user, passes):
            messagebox.showinfo(message = "incorrect login. please try again")
        else:
            messagebox.showinfo(message = f"hi {user}! welcome")
            self.root.destroy()
            self.user = user

    def check(self):
        messagebox.showinfo(message = "please login first")

class message():
    def __init__(self):
        self.show = True

    def check(self):
        messagebox.showinfo(message = "please login first")

    def saved(self):
        messagebox.showinfo(message = "score saved!")
    
comm = chatComm("86.36.42.136", 15112)
comm.startConnection()

def begin():
    win = tkinter.Tk()
    A = start(win, comm)
    win.mainloop()
    return A.user

def please():
    B = message()
    B.check()

def save():
    B = message()
    B.saved()
