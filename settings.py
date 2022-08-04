import tkinter as tk
import tkinter.ttk as ttk
from database import User
from tkinter import PhotoImage, messagebox


class Settings:
    state = 1
    def __init__(self, mainWindow):
        if Settings.state == 1:
            Settings.state = 0

            self.Set_win = tk.Tk()
            #self.Set_win.wm_transient(mainWindow)
            self.Set_win.resizable(0, 0)
            self.Set_win.title("Settings")
            self.Set_win.geometry("800x600+225+70")

            settings_image = PhotoImage(file="images/setting.png")
            self.Set_win.iconphoto(False, settings_image)

            #self.sepatator = ttk.Separator(self.Set_win, orient="vertical")
            #self.sepatator.place(relx=0.30, rely=0.05, relwidth=0.2, relheight=0.9)

            self.STYLER = ttk.Style()
            self.STYLER.configure("H.TLabel", font=("Roboto", 10, "bold"))
            self.STYLER.configure("N.TLabel", font=("Roboto", 10))
            self.STYLER.configure("S.TLabel", font=("Roboto", 9))
            self.STYLER.configure("L.TFrame")
            self.STYLER.configure("C.TFrame")


            self.left_frame = ttk.Frame(self.Set_win, height=600, style="L.TFrame")
            #self.left_frame.place(relx=0, rely=0.00, relwidth=0.3)
            self.left_frame.pack(side="left",fill="y", padx=0.5)

            self.right_frame = ttk.Frame(self.Set_win, style="C.TFrame", height=600)
            self.right_frame.pack(fill="both")

            self.scrollbar = ttk.Scrollbar(self.left_frame, orient="horizontal")
            self.scrollbar.pack(side="bottom", fill="x")

            self.treeview = ttk.Treeview(self.left_frame, height=600)
            self.treeview.bind("<ButtonRelease-1>", self.return_for_window)
            self.treeview.pack(fill="both")


            # parent widget of hierarchical tree view
            self.treeview.insert("", "0", "item1", text="Settings")     

            # first child widget of hierarchical tree view
            self.treeview.insert("", "1", "item2", text="Appearance")
            self.treeview.insert("", "2", "item3", text="Authentication Manager") 

            # second child widget of hierarchical tree view
            self.treeview.insert("", "3", "item4", text="Add User")
            self.treeview.insert("", "4", "item5", text="Modify User")

            # placing each child items in parent widget
            self.treeview.move("item2", "item1", "end")
            self.treeview.move("item3", "item1", "end")
            self.treeview.move("item4", "item3", "end")
            self.treeview.move("item5", "item3", "end")

            self.Set_win.protocol("WM_DELETE_WINDOW", self.close_window)
            self.Set_win.mainloop()
    

    def return_for_window(self, event=None):
        varCheck = self.treeview.focus()
        
        if varCheck == "item2":
            self.apperance()
        if varCheck == "item4":
            self.add_user()
        if varCheck == "item5":
            self.remove_user()


    def apperance(self):

        def ApplyChanges():
            pass

        self.destroy_widgets()
        obj = database.Return_settings("databases/settings.db")
        
        settings = obj.gain_settings()
        
        FONT = ["Calibri", "Helvetica", "Arial", "Roboto", "Segoe UI"]
        
        defaultFont = tk.StringVar()

        ttk.Label(self.right_frame,text="Font", style="H.TLabel", justify="center").place(relx=0.10, rely=0.10, anchor="w")
        ttk.Combobox(self.right_frame, textvariable=defaultFont, values=FONT, state="readonly").place(relx=0.20, rely=0.10, anchor="w")

        backgroundTheme = tk.IntVar()
        backgroundTheme.set(0)
        ttk.Label(self.right_frame, text="Background", style="H.TLabel").place(relx=0.05, rely=0.20, anchor="w")
        ttk.Radiobutton(self.right_frame, variable=backgroundTheme, value=0).place(relx=0.22, rely=0.20, anchor="w")
        ttk.Label(self.right_frame, text="light", style="S.TLabel").place(relx=0.25, rely=0.20, anchor="w")

        ttk.Radiobutton(self.right_frame, variable=backgroundTheme, value=1).place(relx=0.36, rely=0.20, anchor="w")
        ttk.Label(self.right_frame, text="dark", style="S.TLabel").place(relx=0.39, rely=0.20, anchor="w")

        ttk.Button(self.right_frame, text="Apply Changes", command=ApplyChanges).place(relx=0.45, rely=0.30, anchor="w")


    def add_user(self):

        def addUsertoDatabase():
            if self.varUserName.get() == "" or self.varPassWord.get() == "" or self.AuthenticationLevel.get() == "":
                return messagebox.showwarning("WARNING", "PLEASE FILL ALL THE FIELD")
            elif len(self.varUserName.get()) < 5 or len(self.varPassWord.get()) < 5:
                return messagebox.showwarning("WARNING", "SEEMS LIKE LENGHT OF THE USERNAME OR PASSWORD IS LESS THEN 5")
            elif self.varUserName.get() == "admin":
                return messagebox.showwarning("WARNING", "USER ALREADY IN THE DATABASE")
            else:
                objectInsert = User("databases\\user.db")

                usernamelist = objectInsert.getallusername()

                if self.varUserName.get() in usernamelist:
                    return messagebox.showwarning("WARNING", "USER NAME ALREADY EXISTS IN THE DATABASE")
                else:
                    objectInsert.insertuser(self.varUserName.get(), self.varPassWord.get(), self.AuthenticationLevel.get())
            
                    # setting the field empty
                    self.varUserName.set("")
                    self.varUserPassword.set("")
                    self.varUserEmail.set("")

                    return messagebox.showinfo("SUCCESS", "USER INSERTED SUCCESSFULLY")
            

        self.destroy_widgets()

        ttk.Label(self.right_frame, text="Add User", style="H.TLabel").place(relx=0.4, rely=0.04, anchor="w")  

        ttk.Label(self.right_frame, text="User Name", style="H.TLabel", justify="center").place(rely=0.15, relx=0.1, anchor="w")
        self.varUserName = tk.StringVar()
        ttk.Entry(self.right_frame, textvariable=self.varUserName).place(rely=0.15, relx=0.3, anchor="w")

        ttk.Label(self.right_frame, text="Password", style="H.TLabel", justify="center").place(rely=0.25, relx=0.1, anchor="w")
        self.varPassWord = tk.StringVar()
        ttk.Entry(self.right_frame, textvariable=self.varPassWord).place(rely=0.25, relx=0.3, anchor="w")

        ttk.Label(self.right_frame, text="Level", style="H.TLabel", justify="center").place(rely=0.35, relx=0.1, anchor="w")
        self.AuthenticationLevel = tk.StringVar()
        VALUE = ["ADMIN", "WORKER"]
        ttk.Combobox(self.right_frame, textvariable=self.AuthenticationLevel, width=17, state="readonly", values=VALUE).place(rely=0.35, relx=0.3, anchor="w")

        ttk.Button(self.right_frame, text="Add User", command=addUsertoDatabase).place(relx=0.50, rely=0.45, anchor="w")


    def remove_user(self):
        self.destroy_widgets()
    
        ttk.Label(self.right_frame, text="Modify User", style="H.TLabel").place(relx=0.4, rely=0.04, anchor="w") 


    def destroy_widgets(self):
        for widgets in self.right_frame.winfo_children():
            widgets.destroy()


    def close_window(self):
        Settings.state = 1
        self.Set_win.destroy()
        

obj = Settings(None) 

