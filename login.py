import sys
import time
import database
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox 

class Login:
    state = 1
    def __init__(self):
        if Login.state == 1:
            Login.state = 0
            self.Login = tk.Tk()
            self.Login.title("Login")

            titleIcon = tk.PhotoImage(file="images\login_icon.png")
            self.Login.iconphoto(False, titleIcon)

            self.Login.geometry("400x400+400+200")
            self.Login.resizable(False, False)

            self.varUser = tk.StringVar()
            self.varPass = tk.StringVar()

            ttk.Label(self.Login, text="Login Page", font=("Roboto", 15, "bold")).place(x=150, y=40)
            ttk.Label(self.Login, text="Enter UserName", font=("Roboto", 10)).place(x=20, y=120)
            ttk.Entry(self.Login, textvariable=self.varUser, font=("Roboto", 10), width=30).place(x=130, y=120)
            ttk.Label(self.Login, text="Enter Password", font=("Roboto", 10)).place(x=20, y=180)
            ttk.Entry(self.Login, textvariable=self.varPass, font=("Roboto", 10), width=30, show="*").place(x=130, y=180)

            ttk.Button(self.Login, text="Login", command=self.checkCredentials).place(x=270, y=240)
            ttk.Button(self.Login, text="Clear", command=self.clear).place(x=180, y=240)


            self.Login.mainloop()

    def destroyWindow(self, user ):
        messagebox.showinfo("SUCCESS", "LOGIN SUCCESSFULL")
        curDate = time.localtime()
        curTime = time.strftime("%H:%M:%S")

        file1 = open("files/login.txt", "a")
        file1.write(f"""The last logged in " , {curDate[2]} , "/" , {curDate[1]} , "/" ,
                    {curDate[0]} , " -\t" , {curTime} , 'logged by {user}'"\n""")

        file1.close()
        self.Login.destroy()


    def clear(self):
        self.varUser.set("")
        self.varPass.set("")
        

    def checkCredentials(self):
        if self.varUser.get() == "":
            return messagebox.showwarning("WARNING", "PLEASE ENTER USER NAME")
        elif self.varPass.get() == "":
            return messagebox.showwarning("WARNING", "PLEASE ENTER PASSWORD")
        elif self.varUser.get() == "admin" and self.varPass.get() == "admin":
            self.destroyWindow(user="defaultUser")
        else:
            object = database.User("databases/user.db")
            sign = object.getUser(self.varUser.get(), self.varPass.get())
            
            print(sign)

            if sign:
                self.destroyWindow(self.varUser.get())        
            else:
                return messagebox.showwarning("WARNING", "CREDENTIALS IS WRONG")


obj = Login()