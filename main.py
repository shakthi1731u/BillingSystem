try:
    import os
    import sys
    import time
    import database
    import file_writer
    import configparser
    from tkinter import *
    from tkinter.ttk import *
    from customtkinter import *
    from tkinter import font
    from settings import Settings
    from tkinter import messagebox
except ModuleNotFoundError:
    import os
    import sys
    if(os.name=="nt"):
        os.system("files/batch.bat")
    sys.exit()
    


# This function used to control behavior of x button in CTkToplevel function
def change_state(data, window):
    if data == 3:
        global arow
        arow = 1
        window.destroy()
    elif data == 2:
        global add_stock_window
        add_stock_window = 1
        window.destroy()
    elif data == 1:
        global help_window
        help_window = 1
        window.destroy()
    elif data == 4:
        global mwindow
        mwindow = 1
        window.destroy()
    elif data == 5:
        global checkout_window
        checkout_window = 1
        window.destroy()
    elif data == 6:
        global edit_window
        edit_window = 1
        window.destroy()
    elif data == 7:
        global report_window
        report_window = 1
        window.destroy()
    elif data == 10:
        global return_stock_window
        return_stock_window = 1
        window.destroy()
    elif data == 11:
        global search_window
        search_window = 1
        window.destroy()


# This function used to not let the other windows to be opened when one window is 
# in the active state(opened)
def isOpened(event=None):
    global mwindow
    global help_window
    global edit_window
    global search_window
    global report_window
    global checkout_window
    global add_stock_window
    global return_stock_window

    if(help_window==0 or edit_window==0 or search_window==0 or report_window==0 or checkout_window==0 or 
       add_stock_window==0 or return_stock_window==0 or mwindow==0):
        print("Yep")
        return True
    else:
        return False


# This menu is invoked when a item is 
# selected in treeview and get clicked in file->edit button
# This menu is mainly aimed for avoiding duplication of adding same 
# value in the main treeview
def edit_menu(event):
    def update_value():
        if len(qun.get()) == 0:
            return messagebox.showwarning("WARNING", "PLEASE INSERT THE QUANTITY")
        elif str(qun.get()).isalpha():
            return  messagebox.showwarning("WARNING", "QUANTITY CAN'T CONTAIN LETTER")
        elif int(qun.get()) == 0:
            return messagebox.showwarning("WARNING", "QUANTITY IS TOO LOW")
        elif int(qun.get()) > int(ava_quan.get()):
            return messagebox.showwarning("WARNING", "ENTERED QUANTITY IS TOO MUCH THAN AVAILABLE QUANTITY")
        else:
            obj = database.TEMP("databases/temp.db")
            obj.update(qun.get(), row[-1])

            mod_row = (row[0], row[1], row[2], int(qun.get()), row[4], int(qun.get()) * row[4], row[-1])
            
            treeview.item(selected, text="", values=(mod_row))     

            if len(treeview.get_children()) == 0:
                priceEntry.set("0")
            else:
                price = 0
                g_row = list
                for i in treeview.get_children():
                    g_row = treeview.item(i, "values")
                    price = price + int(g_row[5])

                priceEntry.set(price)

            return change_state(6, child9)

    row = selected = treeview.focus()
    
    global edit_window
    if row == "":
        return messagebox.showwarning("WARNING", "PLEASE SELECT THE PRODUCT TO EDIT")
    else:
        row = treeview.item(row)
        row = row["values"]
        print(row)
        if edit_window == 1:
            edit_window += 1
            child9 = CTkToplevel(root)
            child9.wm_transient(root)
            child9.title("EDIT WINDOW")
            child9.configure(background="#edeacc")
            child9.resizable(False, False)
            child9.geometry("600x400+350+100")

            icon = PhotoImage(file="images/icons8-edit.gif")
            child9.iconphoto(False, icon)

    
            CTkLabel(child9, text="EDIT PAGE").pack()

            CTkLabel(child9, text="ID", justify="right").place(anchor="w", relx=0.10, rely=0.15)
            id = StringVar()
            id.set(row[0])
            CTkEntry(child9, textvariable=id, state="readonly", justify="center").place(anchor="w", relx=0.20,
                                                                                           rely=0.15)


            CTkLabel(child9, text="Product Name").place(anchor="w", relx=0.50, rely=0.15)
            pro_name = StringVar()
            pro_name.set(row[1])
            CTkEntry(child9, textvariable=pro_name, state="readonly", justify="center").place(anchor="w", relx=0.65,
                                                                                             rely=0.15)

            CTkLabel(child9, text="Product Size").place(anchor="w", relx=0.05, rely=0.30)
            pro_size = StringVar()
            pro_size.set(row[2])
            CTkEntry(child9, textvariable=pro_size, state="readonly", justify="center").place(anchor="w", relx=0.20, rely=0.30)

            CTkLabel(child9, text="Price").place(anchor="w", relx=0.50, rely=0.30)
            pro_price = StringVar()
            pro_price.set(row[4])
            CTkEntry(child9, textvariable=pro_price, state="readonly", justify="center").place(anchor="w", relx=0.65,
                                                                                           rely=0.30)

            CTkLabel(child9, text="""-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------""", 
                            ).place(anchor="w", rely=0.40)

            obj = database.TEMP("databases//temp.db")

            value  = obj.return_specific(row[-1])
            
            value += int(row[3])
            print(value)

            CTkLabel(child9, text="Available Quantity").place(anchor="w", relx = 0.30, rely = 0.45)
            ava_quan = StringVar()
            ava_quan.set(value)
            CTkEntry(child9, textvariable=ava_quan, width=15, justify="center", state="readonly").place(anchor="w", relx=0.50, rely=0.45)

            CTkLabel(child9, text="Enter the quantity").place(anchor="w", relx=0.05, rely=0.60)
            qun = StringVar()
            CTkEntry(child9, textvariable=qun, justify="right", width=15).place(anchor="w", relx=0.24, rely=0.60)

            CTkButton(child9, text="Update", command=update_value).place(anchor="w", relx=0.45, rely=0.60)

            CTkLabel(child9, text="NOTE ---> (THIS AVAILABLE QUANTITY SHOWS THE ADDITION OF \n \t\t\t\t\t QUANTITY FROM THE MAIN WINDOW)", 
                                                                                ).place(anchor="w", rely=0.80, relx=0.05)

            child9.protocol("WM_DELETE_WINDOW", lambda : change_state(6, child9))
            child9.mainloop()


# remove every values from all fields including Treeview
# Fields are
# 1.) treeview
# 2.) productEntry
# 3.) codeEntry
# 4.) priceEntry
def remove_everything():
    treeview.delete(*treeview.get_children())
    productEntry.set("")
    codeEntry.set("0")
    priceEntry.set("0")

    obj = database.TEMP("databases/temp.db")
    obj.remove_everything()

    return


# remove every values from all fields including Treeview
# Fields are
# 1.) productEntry
# 2.) codeEntry
def set_field_empty():
    productEntry.set("")
    codeEntry.set("0")
    return


# add values to tree by just invoking this
# by supplying required parameters
def add_to_treeview(data):
    # obj = database.TEMP("databases/temp.db")
    # obj.insert(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    i = 1
    # counting how many childrens(rows) in the treeview
    for item in treeview.get_children():
        i += 1

    # setting up the serial number
    data[0] = i
    treeview.insert("", END, values=data)

    # setting up the value in netamount field
    priceEntry.set(str(float(priceEntry.get()) + data[-2]))

    global arow
    arow = 1


# help menu
def help_menu(event=None):
    global help_window

    if help_window <= 1:
        help_window = 2
        child2 = CTkToplevel(root)
        child2.title("Help Menu")
        child2.resizable(False, False)
        child2.geometry("350x200+450+200")

        img = PhotoImage(file="images/information.png")
        child2.iconphoto(False, img)

        CTkLabel(child2, text="This app is designed for educational purpose \n\t in 2022 by sptc students", font=(fontstyle, 13),
              ).place(anchor=W, relx=0.10, rely=0.20)
    
        CTkButton(child2, text="Exit", command=lambda: change_state(1, child2), font=(fontstyle, 13)).place(anchor=W,
                                                                                                      relx=0.35,
                                                                                                      rely=0.50)
        child2.wm_transient(root)
        child2.protocol("WM_DELETE_WINDOW", lambda: change_state(1, child2))
        child2.mainloop()


def close_window2(event=None, window=None):
    yes_or_no = messagebox.askyesno("Ask Question", "Do you want to close the application ? ".upper())
    if yes_or_no:
        window.destroy()
        sys.exit()
    else:
        return


# change the behavior of "X" button of root window
# by prompting yes or no messagebox on the screen
# if yes get clicked then main windows will close else not
def close_window(event=None):  
    obj = database.TEMP("databases/temp.db")
    if len(treeview.get_children()) >= 1:
        yes_or_no = messagebox.askyesno("Ask Question", "Some finished progress is waiting, Do you want to Save to Memory ?".upper())
        if yes_or_no:
            load_to_memory()
            yes_or_no = messagebox.askyesno("Ask Question", "Do you want to close the application ? ".upper())
            if yes_or_no:
                obj.remove_everything()
            sys.exit()
        else:
            yes_or_no = messagebox.askyesno("Ask Question", "Do you want to close the application ? ".upper())
            if yes_or_no:
                obj.remove_everything()
                sys.exit()
            else:
                return
    yes_or_no = messagebox.askyesno("Ask Question", "Do you want to close the application ? ".upper())
    if yes_or_no:
        obj.remove_everything()
        sys.exit()
    else:
        return


# present inside file menu
# for adding stocks
def add_stock(event=None):
    #checking any other child window is in open state
    if(isOpened):
        return

    # this function responsible for validation and insertion of data
    # into database
    def insert():
        obj = database.DataBase1("databases/Database.db")
        row = obj.return_everything()

        if product_name.get() is None:
            return messagebox.showwarning("Warning", "Product name field is empty")
        elif quantity.get() == 0 or quantity.get() < -1:
            return messagebox.showwarning("Warning", "Quantity is 0")
        elif price.get() == 0 or price.get() < -1:
            return messagebox.showwarning("Warning", "Price is 0")
        else:
            obj.insert(code_no.get(), product_name.get(), quantity.get(), short_name.get(), price.get(), pro_size.get())
            messagebox.showinfo("successful", "Product insert successful")

            code_no.set(0)
            product_name.set("")
            quantity.set(0)
            short_name.set("")
            price.set(0)
            pro_size.set("Small")

            return

    global add_stock_window
    global arow

    if arow > 1:
        return messagebox.showwarning("WARNING", "PLEASE ADD TO CART WINDOW")

    if add_stock_window < 2:
        add_stock_window += 1

        child1 = CTkToplevel(root)
        child1.title("Add Stock")
        child1.geometry("500x600+360+90")
        child1.resizable(False, False)

        # variables for holding add stock data
        code_no = IntVar()
        product_name = StringVar()
        quantity = IntVar()
        short_name = StringVar()
        price = IntVar()
        pro_size = StringVar()
        pro_size.set("Small")

        add_icon_image = PhotoImage(file="images/add_icon.png")
        child1.iconphoto(False, add_icon_image)

        CTkLabel(child1, text=" ").pack()
        CTkLabel(child1, text="Add Stock", font=(fontstyle, 15, "bold")).pack()

  
        CTkLabel(child1, text="Enter the code ", justify=LEFT, font=(fontstyle, 13)).place(anchor=W, rely=0.15, relx=0.07)
        CTkEntry(child1, textvariable=code_no, width=245, font=(fontstyle, 13)).place(anchor=W, rely=0.15, relx=0.40)

        CTkLabel(child1, text="Enter the product name ", font=(fontstyle, 13)).place(anchor=W, rely=0.25, relx=0.07)
        CTkEntry(child1, textvariable=product_name, width=245, font=(fontstyle, 13)).place(anchor=W, rely=0.25, relx=0.40)

        CTkLabel(child1, text="Enter the short name ", font=(fontstyle, 13)).place(anchor=W, rely=0.35, relx=0.07)
        CTkEntry(child1, textvariable=short_name, width=245, font=(fontstyle, 13)).place(anchor=W, rely=0.35, relx=0.40)

        CTkLabel(child1, text="Enter quantity", font=(fontstyle, 13)).place(anchor=W, rely=0.45, relx=0.07)
        CTkEntry(child1, textvariable=quantity, width=245, font=(fontstyle, 13)).place(anchor=W, rely=0.45, relx=0.40)

        CTkLabel(child1, text="Enter the price", font=(fontstyle, 13)).place(anchor=W, rely=0.55, relx=0.07)
        CTkEntry(child1, textvariable=price, width=245, font=(fontstyle, 13)).place(anchor=W, rely=0.55, relx=0.40)

        product_size = ["Small", "Medium", "Large", "XLarge"]
        CTkLabel(child1, text="Select the size", font=(fontstyle, 13)).place(anchor=W, rely=0.65, relx=0.07)
        CTkComboBox(child1, variable=pro_size, values=product_size, state="readonly", width=242, font=(fontstyle, 13)).place(anchor=W,
                                                                                                       rely=0.65,
                                                                                                       relx=0.40)

        CTkButton(child1, text="Add Stock", image=add_icon_image, compound=LEFT, command=insert, font=(fontstyle, 13)).place(
            anchor=W, rely=0.80, relx=0.35)

        child1.wm_protocol("WM_DELETE_WINDOW", lambda: change_state(2, child1))
        child1.wm_transient(root)
        child1.mainloop()


# item page CTkToplevel window
def item_page():
    # test for the condition
    # if non of them get satisfied
    # it moves to else part and
    # execute main code
    def move_to_main():
        if pro_name.get() == "":
            return messagebox.showwarning("WARNING", "PLEASE SELECT THE ITEM")
        elif pro_amount.get() == "":
            return messagebox.showwarning("WARNING", "PLEASE ENTER THE QUANTITY")
        elif str(pro_amount.get()).isalpha():
            return messagebox.showwarning("WARNING", "PLEASE ENTER PROPER QUANTITY")
        elif int(data[3]) < int(pro_amount.get()):
            return messagebox.showwarning("WARNING", "ENTERED QUANTITY IS TOO MUCH THAN AVAILABLE QUANTITY")
        else:
            
            # chekcing that the product is already is exists in the treeview
            for i in treeview.get_children():
                j = treeview.item(i)
                j = j["values"]
                if j[-1] == data[-1]:
                    messagebox.showwarning("WARNING", "THIS PRODUCT IS ALL READY EXISTS IN MAIN WINDOW")
                    return

            obj_3 = database.TEMP("databases/temp.db")
            row2 = obj_3.return_everything()

            pos = 0
            if len(row2) != 0:
                for i in row2:
                    if i[0] == data[-1]:
                        obj_3.update(data[-1], data[3] - int(pro_amount.get()))
                        pos = 1
            if pos != 1:
                obj_3.insert_value(data[-1], data[3] - int(pro_amount.get()))

            data[3] = int(pro_amount.get())

            # storing the id value in id_value variable
            # because of some interference

            id_value = data[-1]

            obj2 = database.TEMP("databases/temp.db")

            # this function remove value at the end of the list
            data.pop()

            # multiplies quantity * price and append at the end of list data
            data.append(int(data[3] * data[4]))
            # again inserting at the end of list by append method
            data.append(id_value)

            child3.destroy()
            global open
            open = 1
            return add_to_treeview(data)

    # it is used to get values from
    # treeview1 on child3 and place
    # them in entry field
    # this is invoked when the
    # rows in treeview1 got clicked
    def add_items(event):
        selected_row = treeview1.focus()
        global data
        data = treeview1.item(selected_row)
        data = data['values']

        try:
            int(data[0])
        except IndexError:
            return None

        if int(data[3]) < 1:
            return messagebox.showinfo("INFORMATION", "THIS PRODUCT IS OUT OF STOCK !")


        else:
            pro_name.set(str(data[1]))
            pro_size.set(str(data[2]))

    # inserting the values into
    # treeview1 on child3
    def set_item():
        treeview1.delete(*treeview1.get_children())  # deleting all records in the treeview1

        for rows in row:
            treeview1.insert("", END, values=rows)  # inserting the record in treeview1 which
            # is gained from child3 main function

        sb.config(command=treeview.yview)  # used to invoke scrollbar

    # This is first executed when this function is get invoked
    # If non of these condition get satisfied and moves to else
    # part then it get values from database files and stores
    # in a "row" variable
    obj = database.DataBase1("databases/Database.db")
    obj2 = database.TEMP("databases/temp.db")
    if productEntry.get() == "":
        if codeEntry.get() == "" or codeEntry.get() == "0":
            return messagebox.showwarning("WARNING", "PLEACE INSERT THE KEYWORD")
        elif str(codeEntry.get()).isalpha():
            return messagebox.showwarning("WARNING", "CODE NUMBER CAN'T BE EMPTY")
        else:
            row = obj.return_item("Code_No", codeEntry.get())
            row2 = obj2.return_everything()

            if len(row2) == 0:
                row = obj.return_item("Code_No", codeEntry.get())
            elif len(row2) != 0:
                row3 = []
                count = 0
                for i in row:
                    count = 0
                    for j in row2:
                        print("j = ", j)
                        if j[0] == i[-1]:
                            row3.append([i[0], i[1], i[2], j[1], i[4], i[5]])
                            count = 1
                    if count != 1:
                        row3.append([i[0], i[1], i[2], i[3], i[4], i[5]])
                        count = 0

                row = row3
    else:
        row = obj.return_item("Product_Name", productEntry.get())
        row2 = obj2.return_everything()

        if len(row2) == 0:
            row = obj.return_item("Product_Name", productEntry.get())
        elif len(row2) != 0:
            row3 = []
            count = 0
            for i in row:
                count = 0
                for j in row2:
                    if j[0] == i[-1]:
                        row3.append([i[0], i[1], i[2], j[1], i[4], i[5]])
                        count = 1
                if count != 1:
                    row3.append([i[0], i[1], i[2], i[3], i[4], i[5]])
                    count = 0

            row = row3

    global arow
    if arow < 2:
        arow += 1
        # This is user interfacing decorating part
        # used to fill this screen with text, button,
        # radiobutton, entry etc..  widgets
        child3 = CTkToplevel(root)
        child3.title("Add to cart")
        child3.geometry("800x400+250+100")
        child3.resizable(False, False)
        shoppingcartImage = PhotoImage(file="images/trolly_image.png")
        child3.iconphoto(False, shoppingcartImage)

        top_frame = CTkFrame(child3, height=50)
        top_frame.pack(fill="x")

        labelstyle = Style()

        CTkLabel(top_frame, text="Product Name", font=(fontstyle, 13)).place(anchor=W, relx=0.02, rely=0.40)
        pro_name = StringVar()
        CTkEntry(top_frame, textvariable=pro_name, state="readonly", font=(fontstyle, 13)).place(anchor=W, relx=0.13, rely=0.40)

        CTkLabel(top_frame, text="Product Size", font=(fontstyle, 13)).place(anchor=W, relx=0.32, rely=0.40)
        pro_size = StringVar()
        CTkEntry(top_frame, textvariable=pro_size, state="readonly", font=(fontstyle, 13)).place(anchor=W, relx=0.42, rely=0.40)

        CTkLabel(top_frame, text="Product Quantity", font=(fontstyle, 13)).place(anchor=W, relx=0.61, rely=0.40)
        pro_amount = StringVar()
        CTkEntry(top_frame, textvariable=pro_amount, state="normal", font=(fontstyle, 13)).place(anchor=W, relx=0.75, rely=0.40)

        trframestyle = Style()
        trframestyle.configure("AT.TFrame", background="orange")
        tframe = Frame(child3, style="AT.TFrame", height=200)
        tframe.pack(fill="x")

        sb = Scrollbar(tframe)
        sb.pack(side=RIGHT, fill=Y)

        tvStyle = Style()
        tvStyle.theme_use('default')
        tvStyle.configure('mystylefinaltvTreeview', background='silver',foreground='black',rowheight=23,fieldbackground='silver')
        tvStyle.configure('mystylefinaltv.Treeview',font=(fontstyle,10))
        tvStyle.configure('mystylefinaltv.Treeview.Heading',font=(fontstyle,10,'bold'),justify='center')

        treeview1 = Treeview(tframe, columns=['1', '2', '3', '4', '5'],style="mystylefinaltv.Treeview", yscrollcommand=sb.set, height=14)
        treeview1['show'] = "headings"
        treeview1.heading("1", text="Code No")
        treeview1.column("1", width=100, anchor=CENTER)
        treeview1.heading("2", text="product Name")
        treeview1.column("2", anchor=CENTER)
        treeview1.heading("3", text="Product Size")
        treeview1.column("3", width=140, anchor=CENTER)
        treeview1.heading("4", text="Quantity")
        treeview1.column("4", width=150, anchor=CENTER)
        treeview1.heading("5", text="Price")
        treeview1.column("5", width=120, anchor=CENTER)
        treeview1.bind("<ButtonRelease-1>", add_items)
        treeview1.pack(fill="both")

        bottomFrame = CTkFrame(child3, height=130)
        bottomFrame.pack(fill="both")
        add_icon = PhotoImage(file="images/add_icon.png")
        CTkButton(bottomFrame, text="Add", image=add_icon, compound="left", height= 30,command=move_to_main, font=(fontstyle, 13)).pack(side="right")

        child3.protocol("WM_DELETE_WINDOW", lambda: change_state(3, child3))
        child3.wm_transient(root)  # This is used to make child3 as main window when it is activated or invoked

        set_item()  # Invoke this function which is present in the item_page function

        child3.mainloop()  # Make this windows runs infinite amount of time


# this function used to delete a
# particular row from mainscreen
# treeview
def delete_from_tv():
    selected_row = treeview.focus()  # getting the selected from treeview
    i = treeview.item(selected_row)
    i = i["values"]
    obj = database.TEMP("databases/temp.db")
    try:
        obj.remove_particular(i[-1])
    except IndexError:
        return
    try:
        treeview.delete(selected_row)  # deleting using delete method
    except:
        messagebox.showwarning("WARNING", "Please select a product to be deleted")
        return

    if len(treeview.get_children()) == 0:
        priceEntry.set("0")
    else:
        price = 0
        for i in treeview.get_children():
            row = treeview.item(i)
            row = row['values']
            price = price + int(row[5])

        priceEntry.set(price)
        return


# add_stock()
# how much earn totally, monthly, daily
def report(event=None):
    def set_data():
        
        months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        date = time.localtime()

        obj1 = database.purchased("databases/purchased.db", months[date[1]])
        obj2 = database.Total("databases/total.db")

        total = obj2.return_value()
        ftm = obj1.return_value(months[date[1]])
        
        if total == []:
            return 

        Total_Earning.set(total[0][0])
        tps.set(total[0][1])

        if len(ftm) == 0:
            for_this_month.set(0)
            return 

        for_this_month.set(ftm)
        
        return

    global report_window
    if report_window == 1:
        report_window += 1
        child5 = CTkToplevel(root)
        child5.title("Report")  # Creating Tk object
        child5.wm_transient(root)
        child5.resizable(False, False)
        child5.geometry("400x350+400+150")
        child5.configure(background="#d6d0d0")
        icon = PhotoImage(file="images/report.png")
        child5.iconphoto(False, icon)

        CTkLabel(child5, text="Report").pack()

        CTkLabel(child5, text="Toatal Earnings ").place(anchor="w", rely=0.15, relx=0.05)
        Total_Earning = StringVar() 
        CTkEntry(child5, textvariable=Total_Earning, state="readonly", justify="center").place(anchor="w", rely=0.15, relx=0.36)

        months={1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        date = time.localtime()
    
        string = str(months[date[1]]) +" "+" Month"+" Total"

        CTkLabel(child5, text=string).place(anchor="w", rely=0.30, relx=0.05)
        for_this_month = StringVar()
        CTkEntry(child5, textvariable=for_this_month, state="readonly", justify="center").place(anchor="w", rely=0.30, relx=0.36)

        CTkLabel(child5, text="Total products selled").place(anchor="w", rely=0.45, relx=0.05)
        tps = StringVar()
        CTkEntry(child5, textvariable=tps, state="readonly", justify="center").place(anchor="w", rely=0.45, relx=0.36)

        #CTkLabel(child5, text="Best Selling product").place(anchor="w", rely=0.60, relx=0.05)
        #bsp = StringVar()
        #Entry(child5, text=bsp, state="readonly", justify="center").place(anchor="w", rely=0.60, relx=0.36)

        CTkLabel(child5, text="NOTE --> (THIS WINDOW IS UNDER DEVELOPMENT SO \nWE CAN'T ADD MORE FEATURES TO IT RIGHT. NOW \nMAY BE IN FUTURE WE WILL UPDATE THIS WINDOW IN \nSPTC-2022/GITHUB PAGE)").place(anchor="w", relx=0.05, rely=0.75)

        set_data()

        child5.protocol("WM_DELETE_WINDOW", lambda : change_state(7, child5))
        child5.mainloop()  # Make this windows runs infinite amount of time


# this function is responsible for
# updation and deletion
# this place is responsible for some
# advance search and core modification
def maintain_stock(event=None):
    def set_data_3(even=None):

        data = treeview3.focus()
        data = treeview3.item(data, "values")

        try:
            data[0]
        except IndexError:
            return

        c_no.set(data[0])
        p_name.set(data[1])
        p_short_name.set(data[2])
        quan.set(data[3])
        price.set(data[4])
        size.set(data[5])
        id.set(data[6])
        return 

    def search():
        def add_to_treeview3(data):
            treeview3.delete(*treeview3.get_children())

            for i in data:
                treeview3.insert("", END, values=i)

            return
        
        if keyword.get() == "":
            return messagebox.showwarning("WARNING", "PLEASE INSERT SOME KEYWORD")
        else:
            obj = database.DataBase1("databases/Database.db")
            if search_by.get() == "code no":
                row = obj.return_specific("Code_No", keyword.get())
            elif search_by.get() == "pro name":
                row = obj.return_specific("Product_Name", keyword.get())
            elif search_by.get() == "pro size":
                row = obj.return_specific("Product_size", keyword.get())
            
        if row == []:
            return
        else:
            global word
            global key
            key = search_by.get()
            word = keyword.get()
            add_to_treeview3(row)

    def update_data():
        if len(treeview3.get_children()) == 0:
            return messagebox.showwarning("WARNING", "PLEASE SEARCH FOR SOME ID")
        row = treeview3.focus()
        print(row)
        if row == "":
            return messagebox.showwarning("WARNING", "PlEASE SELECT A ROW")

        obj = database.DataBase1("databases/Database.db")
        ver = obj.update_2(c_no.get(), p_name.get(), p_short_name.get(), quan.get(), price.get(), size.get(), id.get())

        messagebox.showinfo("SUCCESS", "DATAS ARE SUCCESSFULLY UPDATED")
        
        global word
        global key

        obj = database.DataBase1("databases/Database.db")
        if key == "code no":
            row = obj.return_specific("Code_No", word)
        elif key == "pro name":
            row = obj.return_specific("Product_Name", word)
        elif key == "pro size":
            row = obj.return_specific("Product_size", word)

        treeview3.delete(*treeview3.get_children())

        for i in row:
            treeview3.insert("", END, values=i)

        c_no.set("")
        p_name.set("")
        p_short_name.set("")
        quan.set("")
        price.set("")
        size.set("")
        id.set("")
        return     

    def delete_data():
        if len(treeview3.get_children()) == 0:
            return messagebox.showwarning("WARNING", "PLEASE SEARCH FOR SOME ID")
        row = treeview3.focus()
        print(row)
        if row == "":
            return messagebox.showwarning("WARNING", "PlEASE SELECT A ROW")

        obj_temp = database.TEMP("databases/temp.db")
        value = obj_temp.return_everything()
        for_del = row
        row  = treeview3.item(row, "values")
        
        for i in value:
            if i[0] == int(row[-1]):
                check = messagebox.askyesno("QUESTION", "THIS PRODUCT IS PRESENT IN MEMORY DO YOU WANT TO STILL DELETE")
                if not check:
                    return
                else:
                    obj_temp.remove_particular(row[-1])
                    treeview.delete(for_del)

                    price = 0
                    for i in treeview.get_children():
                        row = treeview.item(i)
                        row = row['values']
                        price = price + int(row[5])

                    priceEntry.set(price)

        obj = database.DataBase1("databases/Database.db")    
        ver = obj.delete_by_id(id.get())
        if ver:
            messagebox.showinfo("SUCCESS", "DATAS ARE SUCCESSFULLY DELETED")

        global word
        global key

        obj = database.DataBase1("databases/Database.db")
        if key == "code no":
            row = obj.return_specific("Code_No", word)
        elif key == "pro name":
            row = obj.return_specific("Product_Name", word)
        elif key == "pro size":
            row = obj.return_specific("Product_size", word)

        treeview3.delete(*treeview3.get_children())
        if row == []:
            return
        else:
            for i in row:
                treeview3.insert("", END, values=i)

            c_no.set("")
            p_name.set("")
            p_short_name.set("")
            quan.set("")
            price.set("")
            size.set("")
            id.set("")
            return    

    if(isOpened):
        return         

    global mwindow
    if mwindow==1:
        mwindow=0
        child6 = CTkToplevel(root)  # creating Tk object
        child6.wm_transient(root)  # This is used to make child6 as main window when it is activated or invoked
        child6.title("Maintain Stock")  # This function is used to add title to this child6 window
        child6.resizable(False, False)  # This function set false on height width resize
        child6.geometry("1100x650+100+45")  # This is used to set the screen height and width   

        id = StringVar()

        top_frame = CTkFrame(child6, height=100)
        top_frame.pack(fill="x")

        body_frame = CTkFrame(child6, height=150)
        body_frame.pack(fill="x")

        CTkLabel(top_frame, text="MAINTAIN STOCK", font=(fontstyle, 13, "bold")).pack()

        CTkLabel(body_frame, text="Code No", font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.03)
        c_no = StringVar()
        CTkEntry(body_frame, textvariable=c_no, font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.08)

        CTkLabel(body_frame, text="Product Name", font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.22)
        p_name = StringVar()
        CTkEntry(body_frame, textvariable=p_name, font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.30)

        CTkLabel(body_frame, text="Product Short Name", font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.44)
        p_short_name = StringVar()
        CTkEntry(body_frame, textvariable=p_short_name, font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.56)

        CTkLabel(body_frame, text="Quantity", font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.71)
        quan = StringVar()
        CTkEntry(body_frame, textvariable=quan, font=(fontstyle, 13)).place(anchor="w", rely=0.23, relx=0.76)

        CTkLabel(body_frame, text="Price", font=(fontstyle, 13)).place(anchor="w", rely=0.55, relx=0.30)
        price = StringVar()
        CTkEntry(body_frame, textvariable=price, font=(fontstyle, 13)).place(anchor="w", rely=0.55, relx=0.34)

        CTkLabel(body_frame, text="Size", font=(fontstyle, 13)).place(anchor="w", rely=0.55, relx=0.48)
        size = StringVar()
        CTkEntry(body_frame, textvariable=size, font=(fontstyle, 13)).place(anchor="w", rely=0.55, relx=0.52)

        CTkLabel(body_frame, text="Keyword", font=(fontstyle, 13)).place(anchor="w", rely=0.90, relx=0.63)
        keyword = StringVar()
        CTkEntry(body_frame, textvariable=keyword, justify="right", font=(fontstyle, 13)).place(anchor="w", rely=0.90, relx=0.68)

        search_by = StringVar()
        search_by.set("code no")
        CTkComboBox(body_frame, variable=search_by, values=["code no", "pro name", "pro size"],
        width=90, state = "readonly", font=(fontstyle, 13)).place(anchor="w", rely=0.90, relx=0.81)
        CTkButton(body_frame, text="SEARCH", command=search, font=(fontstyle, 13), width=30).place(anchor="w", rely=0.90, relx=0.90)

        CTkButton(body_frame, text="UPDATE", command=update_data, font=(fontstyle, 13), width=30).place(anchor="w", rely=0.90, relx=0.03)
        CTkButton(body_frame, text="DELETE", command=delete_data, font=(fontstyle, 13), width=30).place(anchor="w", rely=0.90, relx=0.10)

        tv3frame = Frame(child6, style="TV.TEntry", height=470)
        tv3frame.pack(fill="x")

        scrollbar = CTkScrollbar(tv3frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        tvstyle = Style()
        tvstyle.configure("mystyle.Treeview", font=(fontstyle, 10))
        tvstyle.configure("mystyle.Treeview.Heading", font=(fontstyle, 10, "bold"), justify="center")

        treeview3 = Treeview(tv3frame, style="mystyle.Treeview", column=["1", "2", "3", "4", "5", "6"],
                            yscrollcommand=scrollbar.set, height=22)
        
        treeview3["show"] = "headings"
        treeview3.heading("1", text="Code No")
        treeview3.column("1", width=100, anchor=CENTER)
        treeview3.heading("2", text="Product Name")
        treeview3.column("2", width=150, anchor=CENTER)
        treeview3.heading("3", text="Short Name")
        treeview3.column("3", width=100, anchor=CENTER)
        treeview3.heading("4", text="Quantity")
        treeview3.column("4", width=100, anchor=CENTER)
        treeview3.heading("5", text="Price")
        treeview3.column("5", width=100, anchor=CENTER)
        treeview3.heading("6", text="Size")
        treeview3.column("6", width=150, anchor=CENTER)
        treeview3.bind("<ButtonRelease-1>", set_data_3)
        treeview3.pack(fill="x")

        child6.wm_protocol("WM_DELETE_WINDOW", lambda: change_state(4, child6))
        child6.mainloop()  # Make this windows runs infinite amount of time


# this function takecare of reducing
# amount of item and responsible for
# creating bill
def checkout():
    def billed():
        yes_or_no = messagebox.askyesno("Question", "Do you want to proceed ? ")
        # creating object with database "Database"
        if not yes_or_no:
            return

        obj = database.DataBase1("databases/Database.db")

        # getting values from main treeview
        data = []
        for i in treeview.get_children():
            row = treeview.item(i)
            data.append(row["values"])

        # getting the total quantity
        row = []
        for i in range(len(data)):
            this = obj.return_for_bill(data[i][-1])
            row.append(this)

        # removing the current quantity with available quantity
        new_row = [];
        j = 0;
        length = 0

        for i in row:
            for j in i:
                new_row.append([j[0] - data[length][3], j[1]])
            length += 1

        # updating the values
        for i in new_row:
            print(i)
            obj.update(i[0], i[1])

        
        total_products = 0
        data = []
        bill_data = []
        return_row = []
        for i in treeview2.get_children():
            j = treeview2.item(i)
            j = j["values"]
            return_row.append(j)
            print("return_row", return_row)
            total_products += j[2]
            data.append([j[1], j[3]])


        obj.close_con()  # cosing the connection with database

        months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        date = time.localtime()

        obj_report = database.purchased("databases/purchased.db", months[date[1]])

        if obj_report.check_state( months[date[1]]) == False:
            obj_report.insert(months[date[1]], total_var.get())
        else:
            value = obj_report.return_value(months[date[1]])
            print(total_var.get())
            obj_report.update(months[date[1]], int(total_var.get()) + int(value[0][0]))

        obj_report_2 = database.Total("databases/total.db")

        if obj_report_2.check_state() == False:
            obj_report_2.insert(total_var.get(), total_products)
        else:
            var = obj_report_2.return_value()
            total_earnings = var[0][0] + int(total_var.get())
            total_selled_products = var[0][1] + total_products

            obj_report_2.update(total_earnings, total_selled_products)

        obj_return = database.Return_products("databases/return.db")
        
        for value in return_row:
            obj_return.insert(value[0], value[1], value[2], value[3], value[-1], Bill_no.get())


        yes_or_no = messagebox.askyesno("Question", "Do you want to print bill ?")

        # if the answer is true then bill file is update will with the currenct data
        if yes_or_no:
            obj_2 = file_writer.File_writer(0, data, total=total_var.get())
            time.sleep(2)
            messagebox.showinfo("SUCCESS", "BILLED SUCCESSFULLY")
            time.sleep(2)
            obj_3 = database.TEMP("databases/temp.db")
            obj_3.remove_everything()
            remove_everything()
            change_state(5, child8)
        else:
            messagebox.showinfo("SUCCESS", "BILLED SUCCESSFULLY")
            obj_3 = database.TEMP("databases/temp.db")
            obj = database.Bill_no("databases/Bill_no.db")
            bill_no = obj.return_no()
            var = bill_no[0][0]; var+=1
            obj.update(var)
            obj_3.remove_everything()
            remove_everything()
            change_state(5, child8)

    # this function used to create bill no 
    # to indentify each and every bill with 
    # the number 
    def bill_no_creation():
        obj = database.Bill_no("databases/BIll_no.db")
        row = obj.return_no()
        if row == []:
            obj.insert("100000")
            Bill_no.set("100000")
        else:
            Bill_no.set(row[0][0])


    def apply_discount():
        if dis_value.get() == "":
            return messagebox.showwarning("Warning", "Please insert discount %")
        else:
            value = float(total_var.get()) * (float(dis_value.get()) / 100.0)
            value = float(total_var.get()) - value
            total_var.set(int(value))
            dis_value.set("")


    def set_data_2():
        treeview2.delete(*treeview2.get_children())
        data_1 = []
        row = treeview.get_children()
        for i in range(len(row)):
            rows = treeview.item(row[i])
            data_1.append(rows["values"])

        # removing unnecessary values from the list
        for i in range(len(data_1)):
            row = data_1[i]
            row.pop(2)
            data_1[i] = row

        for rows in data_1:
            treeview2.insert("", END, values=rows)

    if len(treeview.get_children()) < 1:
        return messagebox.showwarning("Warning", "Please add products to the window")

    global checkout_window

    if checkout_window < 2:
        checkout_window += 1
        child8 = CTkToplevel(root)
        child8.wm_transient(root)
        child8.resizable(False, False)
        child8.title("BILL PREVIEW")
        child8.geometry("700x600+300+100")

        TOP_frame = CTkFrame(child8, height=100)
        TOP_frame.pack(fill=X)

        MID_frame = CTkFrame(child8, height=100)
        MID_frame.pack(fill=X)

        scrollbar = CTkScrollbar(MID_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        CTkLabel(TOP_frame, text="BILL PREVIEW", font=(fontstyle, 13, "bold")).place(anchor="w", relx=0.40, rely=0.10)

        CTkLabel(TOP_frame, text="BILL NO", font=(fontstyle, 13)).place(anchor="w", rely=0.80, relx=0.02)
        Bill_no = StringVar()
        CTkEntry(TOP_frame, textvariable=Bill_no, state="readonly", justify="center", font=(fontstyle, 13)).place(anchor="w", rely=0.80,
                                                                                         relx=0.10)

        CTkLabel(TOP_frame, text="DATE", font=(fontstyle, 13)).place(anchor="w", rely=0.80, relx=0.72)
        Date = StringVar()
        date = time.localtime()
        date = str(date[2]), "/", str(date[1]), "/", str(date[0])
        Date.set(date)
        CTkEntry(TOP_frame, textvariable=Date, state="readonly", justify="center", font=(fontstyle, 13)).place(anchor="w", rely=0.80, relx=0.78)

        # pre_arrow_image = PhotoImage(file="images/pre_arrow_image.png")
        # Button(TOP_frame, image=pre_arrow_image).place(anchor="w", rely=0.20)

        # treeview to show the preview of bill page
        treeview2 = Treeview(MID_frame, column=['1', '2', '3', '4'], height=20, yscrollcommand=scrollbar.set,
                             style="MYstyle.Treeview")
        treeview2['show'] = "headings"
        treeview2.heading("1", text="S.NO")
        treeview2.column("1", width=100, anchor="center")
        treeview2.heading("2", text="Product Name")
        treeview2.column("2", anchor="center")
        treeview2.heading("3", text="Quantity")
        treeview2.column("3", width=150, anchor="center")
        treeview2.heading("4", text="Product Price")
        treeview2.column("4", width=150, anchor="center")
        treeview2.pack(fill="both")

        scrollbar.configure(command=treeview2.yview)

        set_data_2()
        bill_no_creation()

        dis_value = StringVar()
        CTkEntry(child8, textvariable=dis_value, width=10, justify="right", font=(fontstyle, 13)).place(anchor="w", rely=0.950, relx=0.015)
        CTkButton(child8, text="Apply Discount", command=apply_discount, font=(fontstyle, 13)).place(anchor="w", rely=0.950, relx=0.01)

        total_var = StringVar()
        edit = float(priceEntry.get())
        edit = int(edit)
        total_var.set(edit)
        CTkLabel(child8, text="TOTAL", font=(fontstyle, 13)).place(anchor="w", rely=0.950, relx=0.72)
        CTkEntry(child8, textvariable=total_var, state="readonly", justify="right", font=(fontstyle, 13)).place(anchor="w", rely=0.950,
                                                                                       relx=0.79)

        af_arrow_image = PhotoImage(file="images/af_arrow_image.png")
        CTkButton(child8, image=af_arrow_image, text="", width=30,command=billed, font=(fontstyle, 13)).place(anchor="w", rely=0.03, relx=0.90)

        child8.protocol("WM_DELETE_WINDOW", lambda: change_state(5, child8))
        child8.mainloop()


# this stores the data from the treeview to database 
# for temproraly and get deleted or update using 
# delete_momory and return_from_memory function 
def load_to_memory(event=None):
    obj = database.load_to_memory("databases/memory.db")
    if len(treeview.get_children()) == 0: 
        return messagebox.showinfo("INFO", "MAIN WINDOW IS EMPTY")
    elif obj.check_state():
        yes_or_no = messagebox.askyesno("INFO", "THIS CONTAIN DATA DO YOU WANT TO OVER WRITE ?")  
        if yes_or_no == False:
            return 
        else:
            obj.delete_memory()

    for i in treeview.get_children():
        row = treeview.item(i, "values")
        
        obj.insert(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    messagebox.showinfo("SUCCESS", "DATA'S STORED IN MEMORY SUCCESSFULLY")

    obj2 = database.TEMP("databases/temp.db")
    obj2.remove_everything()
    #for item in treeview.get_children():
    #   treeview.delete(item)
    return remove_everything()


# this function remove everything from temp database
def delete_memory(event=None):
    obj = database.load_to_memory("databases/memory.db")
    if obj.check_state():
        ok_cancel = messagebox.askokcancel("WARNING", "THIS DELETE EVERYTHING FROM MEMORY ? ") 
        if ok_cancel:
            obj.delete_memory()
            return messagebox.showinfo("SUCCESS", "MEMORY IS EMPTY")
        else:
            return
    elif obj.check_state() == False:
        return messagebox.showinfo("INFO", "MEMORY IS EMPTY")
        

# this funciton get back all the data which stores in temp
# database 
def return_from_memory(event=None):
    obj = database.load_to_memory("databases/memory.db")
    obj2 = database.DataBase1("databases/Database.db")
    obj3 = database.TEMP("databases/temp.db")   

    if obj.check_state() == False:
        return messagebox.showinfo("INFO", "MEMORY IS EMPTY")    
    else:
        row = obj.return_everything()
        state = 0

        n_row = []
        
        # checing that products in memory is greater then 
        # products in available quantity if true 
        # the products is removed from appendation of 
        # treeview and notify the user by messagebox
        # function 

        obj3.remove_everything()
        
        for i in row:
            data = obj2.return_for_bill(i[-1])
            print("data = ",data)

            if data[0][0] < i[3]:
                state = 1   
                continue
            else:
                n_row.append(i)
                obj3.insert_value(i[-1], data[0][0] - i[3])
            

        if len(n_row) == 0:
            obj.delete_memory()
            return messagebox.showinfo("MESSAGE", "PRODUCTS IN THE MEMORY HAVE HIGHER PRODUCT QUANTITY")

        count = []
        j = 1
        for i in n_row:
            count.insert(j-1, [j, i[1], i[2], i[3], i[4], i[5], i[6]]) 
            treeview.insert("", END, values=count[j-1])
            j+=1
        
        price = 0
        for i in treeview.get_children():
            row = treeview.item(i)
            row = row['values']
            price = price + int(row[5])

        priceEntry.set(price)

        obj.delete_memory()

        if state == 1:
            return messagebox.showinfo("MESSAGE", "SOME OF THE PRODUCTS IN THE MEMORY HAVE HIGHER QUANTITY")
        return


def return_stock(event=None):
    def return_item():
        if len(treeview4.get_children()) == 0:
            return messagebox.showwarning("WARNING", "PlEASE SEARCH FOR BILL NO")
        elif return_quan.get() == "" or 0:
            return messagebox.showwarning("WARNING", "PlEASE ENTER PROPER QUANTITY")
        elif str(return_quan.get()).isalpha():
            return messagebox.showinfo("WARNING", "THIS CONTAIN SOME CHARACTER")
        else:
            row = treeview4.focus()
            row = treeview4.item(row, "values")
            
            if int(row[2]) < int(return_quan.get()):
                return messagebox.showwarning("WARNING", "ENTERED QUANTITY IS TOO MUCH THAN AVAILABLE QUANTITY")
            else:
                obj = database.Return_products("databases/return.db")
                print(row, return_quan.get())

                reduced_amound = int(row[2]) - int(return_quan.get())

                obj2 = database.DataBase1("databases/Database.db")
                value = obj2.return_for_bill(row[-2])
                print(value)
                
                data = int(value[0][0]) + int(return_quan.get())
                obj2.update(data, row[-2])

                obj.update(reduced_amound, pri_id = int(row[-1]))


            obj = database.Return_products("databases/return.db")

            row = obj.return_value(int(bill_no.get()))
        
            treeview4.delete(*treeview4.get_children())
            
            for i in row:
                treeview4.insert("", END, values=i)
            
            bill_row = []
            total = 0
            check = messagebox.askyesno("QUESTION", "DO YOU WANT TO PRINT BILL ?")
            if check:
                for i in treeview4.get_children():
                    i = treeview4.item(i, "values")
                    if int(i[2]) == 0:
                        continue
                    else:
                        bill_row.append((i[1], i[3]))
                        total += int(i[3])

                if total == 0:
                    check = messagebox.showinfo("INFORMATION", "TOTAL VALUE IS 0 SO PRINTING BILL IS IMPOSSIBLE !")
                    return    
                else:
                    print(total)
                    obj_print = file_writer.File_writer(bill_no.get() , bill_row, total = total)
            else:
                messagebox.showinfo("SUCCESS", "CHANGES MADE SUCCESSFULLY")
                quan.set("")
                return_quan.set("")
                return
    
    def set_data(event):
        row = treeview4.focus()
        row = treeview4.item(row, "values")
        if int(row[2]) == 0:
            return messagebox.showinfo("INFORMATION", "QUANTITY IS '0'")
        quan.set(row[2])
        return
        
    def search_id():
        if bill_no.get() == "":
            return messagebox.showwarning("WARNING", "BILL NUMBER IS EMPTY") 
        
        obj = database.Return_products("databases/return.db")
        row = obj.return_value(int(bill_no.get()))
        
        treeview4.delete(*treeview4.get_children())

        if len(row) == 0:
            return messagebox.showinfo("NOT FOUND", "BILL NOT FOUND")
        else:
            for i in row:
                treeview4.insert("", END, values=i)

    global return_stock_window
    if return_stock_window ==1:
        return_stock_window = 0
        child10 = CTkToplevel(root)
        child10.title("Return Stock")
        child10.geometry("400x600+450+50")
        child10.resizable(False, False)

        top_frame = CTkFrame(child10, height=75)
        top_frame.pack(fill="x")

        body_frame = CTkFrame(child10, height=500)
        body_frame.pack(fill="x")

        last_frame = CTkFrame(child10, height=50)
        last_frame.pack(fill="both", side="bottom")

        CTkLabel(top_frame, text="RETURN ITEM", font=(fontstyle, 13, "bold")).place(anchor="w", rely=0.10, relx=0.35)

        CTkLabel(top_frame, text="BILL NO", font=(fontstyle, 13)).place(anchor="w", rely=0.65, relx=0.15)
        bill_no = StringVar()
        CTkEntry(top_frame, textvariable=bill_no, justify="right", font=(fontstyle, 13)).place(anchor="w", rely=0.65, relx=0.30)
        search_image = PhotoImage(file="images/search_image.png")
        CTkButton(top_frame, text="SEARCH",command=search_id, font=(fontstyle, 13), width=40).place(anchor="w", rely=0.65, relx=0.68)

       
                
        CTkLabel(last_frame, text="QUAN", font=(fontstyle, 13)).place(anchor="w", rely=0.40, relx=0.05)
        quan = StringVar()
        CTkEntry(last_frame, textvariable=quan, width=90, justify="center", state="readonly", font=(fontstyle, 13)).place(anchor="w", rely=0.40, relx=0.16)

        CTkLabel(last_frame, text="-------------", font=(fontstyle, 13)).place(anchor="w", rely=0.40, relx=0.40)

        return_quan = StringVar()
        CTkEntry(last_frame, textvariable=return_quan, width = 50, font=(fontstyle, 13)).place(anchor="w", rely=0.40, relx=0.55)
        
        CTkButton(last_frame, text="RETURN", command=return_item, font=(fontstyle, 13), width=30).place(anchor="w", rely=0.40, relx=0.70)

        scrollbar = CTkScrollbar(body_frame)
        scrollbar.pack(side="right", fill="y")
        
        tvStyle = Style()
        
        tvStyle.configure("mystyle.Treeview", font=(fontstyle, 10))
        tvStyle.configure("mystyle.Treeview.Heading", font=(fontstyle, 10, "bold"), justify="center")
        
        treeview4 = Treeview(body_frame, columns=["1", "2", "3", "4"], yscrollcommand=scrollbar.set, height=21)

        treeview4['show'] = "headings"
        treeview4.heading("1", text="S.NO")
        treeview4.column("1", width=70, anchor="center")
        treeview4.heading("2", text="Product")
        treeview4.column("2", width=150, anchor="center")
        treeview4.heading("3", text="Quan")
        treeview4.column("3", width=80, anchor="center")
        treeview4.heading("4", text="Price")
        treeview4.column("4", width=80, anchor="center")
        treeview4.bind("<ButtonRelease-1>", set_data)
        treeview4.pack(fill="both")

        child10.protocol("WM_DELETE_WINDOW", lambda : change_state(10, child10))
        child10.wm_transient(root)
        child10.mainloop()

#def unknow_item(self):
    
def search_menu(event=None):
    
    global search_window
    if search_window == 1:
        search_window = 0
        child11 = CTkToplevel(root)
        child11.title("Search")
        child11.geometry("600x600+400+50")
        child11.resizable(False, False)



        child11.protocol("WM_DELETE_WINDOW", lambda : change_state(11, child11))
        child11.wm_transient(root)
        child11.mainloop()


def change_appearance(choosen_theme, event=None):
    global theme
    global config

    if(choosen_theme == "dark" and theme=="light"):
        theme = "dark"
        config.set("SectionOne","theme",choosen_theme)
        print("it is happened")
    if(choosen_theme == "light" and theme=="dark"):
        theme = "light"
        config.set("SectionOne","theme",choosen_theme)

    with open('files/configuration.ini', 'w') as configfile:
                config.write(configfile)
                
    set_appearance_mode(choosen_theme)


def change_font(new_font):
    config = configparser.ConfigParser()
    config.read("files/configuration.ini")
    config.set("SectionTwo","font",new_font)

    with open('files/configuration.ini', 'w') as configfile:
                config.write(configfile)

    global fontstyle
    fontstyle = new_font
    root.update_idletasks()
    messagebox.showinfo("INFO","RESTART THE PROGRAM TO SEE THE CHANGES")
   

if __name__ == '__main__':
    #loading the needed meta for program
    global config
    config = configparser.ConfigParser()
    config.read("files/configuration.ini")
    global theme
    theme = config.get("SectionOne","theme")
    global fontstyle
    fontstyle = config.get("SectionTwo","font")

    #login()
    # '''
    global arow
    global grow
    global c_row
    global word
    global key
    global verify
    global mwindow
    global help_window
    global edit_window
    global search_window
    global report_window
    global checkout_window
    global add_stock_window
    global return_stock_window

    crow = []
    arow = 1
    word = ""
    mwindow = 1
    report_window = 1
    help_window = 1
    edit_window = 1
    search_window = 1
    checkout_window = 1
    add_stocK_window = 1
    return_stock_window = 1

    # remove everything from temprorary 
    obj_remove = database.TEMP("databases/temp.db")
    obj_remove.remove_everything()

    # building main window and decorating with attributes that require to build application
    root = CTk()
    set_appearance_mode(theme)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("{}x{}+{}+{}".format(screen_width, screen_height, -10, -2))

    #changin the default font style of the page.
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family=fontstyle, weight="bold")

    root.title("Billing System")
    root.resizable(True, True)
    titleImage = PhotoImage(file="images/title_icon.png")
    root.iconphoto(False, titleImage)

    # storing screen height and width to variables
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    #changing the font style of menubar in tkinter
    root.option_add("*Menu.font", (fontstyle, 10))

    # adding menus namely help and exit
    menubar = Menu(root, activebackground="orange")
    menubar.config(font=(fontstyle, 10))
    # file menu
    file = Menu(menubar, tearoff=0, relief=RIDGE, activebackground="orange")
    file.config(font=(fontstyle, 10))
    # edit menu
    edit = Menu(menubar, tearoff=0, relief=RIDGE, activebackground="orange")
    # inventory menu
    inventory = Menu(menubar, tearoff=0, relief=RIDGE, activebackground="orange")
    #search menu
    search = Menu(menubar, tearoff=0, relief=RIDGE,activebackground="orange")
    # help menu
    help = Menu(menubar, tearoff=0, relief=RIDGE, activebackground="orange")
    # memory menu
    memory = Menu(menubar, tearoff=0, relief=RIDGE, activebackground="orange")

    menubar.add_cascade(label="File", menu=file)
    # menubar.add_cascade(label="Edit", menu=edit, command=edit)
    menubar.add_cascade(label="Inventory", menu=inventory)
    menubar.add_cascade(label="Search", menu=search)
    menubar.add_cascade(label="Memory", menu=memory)
    menubar.add_cascade(label="Help", menu=help)

    file.add_command(label="Clear All", command=remove_everything)
    file.add_command(label="Clear Fields", command=set_field_empty)
    file.add_separator()
    file.add_command(label="Edit                             Ctrl+E", command=lambda: edit_menu(None))
    file.add_separator()
    

    """ file.add_command(label="Fonts", command=appearance) """
    #creating sub menu for font menu
    fontMenu = Menu(file,tearoff=0, relief=RIDGE, activebackground="orange")
    file.add_cascade(label="Fonts", menu=fontMenu)
    fontMenu.add_command(label="Roboto", font=("Roboto", 10), command=lambda: change_font("Roboto"))
    fontMenu.add_command(label="Times New Roman", font=("Times New Roman", 10), command=lambda: change_font("Times New Roman"))
    fontMenu.add_command(label="Arial",font=("Arial", 10), command=lambda: change_font("Segoe UI"))
    fontMenu.add_command(label="Calibri", font=("Calibri", 10),command=lambda: change_font("Calibri"))

    #creating sub menu for theme menu
    themeMenu = Menu(file,tearoff=0, relief=RIDGE, activebackground="orange")
    file.add_cascade(label="Theme", menu=themeMenu)
    themeMenu.add_command(label="Light", command=lambda: change_appearance(choosen_theme="light"))
    themeMenu.add_command(label="Dark", command=lambda: change_appearance(choosen_theme="dark"))
    
    file.add_separator()
    file.add_command(label="Exit                             Alt+F4", command=close_window)

    

    # edit.add_command(label="Edit", command=edit)

    # help.add_command(label="Manual")
    help.add_command(label="Report                       Ctrl+R", command=report)
    help.add_separator()
    help.add_command(label="About                         F1", command=help_menu)

    inventory.add_command(label="Add Stock                Ctrl+A", command=add_stock)
    inventory.add_command(label="Maintain Stock       Ctrl+M", command=maintain_stock)
    inventory.add_command(label="Return Item             Ctrl+I", command=return_stock)
    #inventory.add_command(label="Unknow Item             Ctrl+U", command=unknown)

    search.add_command(label="Search Record             ", command=search_menu)

    memory.add_command(label="Load to Memory                    Shift+L", command=load_to_memory)
    memory.add_command(label="Return from Memory            Shift+R", command=return_from_memory)
    memory.add_command(label="Delete Memory                      Shift+D", command=delete_memory)

    headFrame = CTkFrame(root, height=50)
    headFrame.pack(fill=X)
    headLabel = CTkLabel(headFrame, text="Billing Page", font=(fontstyle, 15, "bold"))

    firstrowFrame = CTkFrame(root, height=100)
    firstrowFrame.pack(fill=X)

    # widgets for main windows
    productEntry = StringVar()
    productName = CTkLabel(firstrowFrame, text="Product Name", font=(fontstyle, 15))
    CTkEntry(firstrowFrame, width=420, textvariable=productEntry, font=(fontstyle, 15)).place(anchor=W, relx=0.13, rely=0.40)

    codeEntry = StringVar()
    codeEntry.set("0")
    codeNumber = CTkLabel(firstrowFrame, text="Code Number", font=(fontstyle, 15))
    CTkEntry(firstrowFrame, width=420,textvariable=codeEntry, font=(fontstyle,15)).place(anchor=W, relx=0.53, rely=0.40)

    searchImage = PhotoImage(file="images/search_image.png")
    searchButton = CTkButton(firstrowFrame, text="Search", image=searchImage, compound="left", command=item_page, font=(fontstyle, 15))


    tvStyle = Style()
    tvStyle.theme_use('default')
    tvStyle.configure('Treeview', background='silver',foreground='black',rowheight=21,fieldbackground='silver')
    tvStyle.configure('mystyle.Treeview',font=(fontstyle,10))
    tvStyle.configure('mystyle.Treeview.Heading',font=(fontstyle,10,'bold'),justify='center')

    tvFrame = CTkFrame(root, height=200)
    tvFrame.pack(fill=X)
    tvscrollbar = CTkScrollbar(tvFrame)
    tvscrollbar.pack(side=RIGHT, fill=Y)

    treeview = Treeview(tvFrame, column=['1', '2', '3', '4', '5', '6'],
                        style="mystyle.Treeview", height=23, yscrollcommand=tvscrollbar.set)
    treeview['show'] = "headings"
    treeview.heading("1", text="S.NO")
    treeview.column("1", anchor="center")
    treeview.heading("2", text="Product Name")
    treeview.column("2", anchor="center")
    treeview.heading("3", text="Size")
    treeview.column("3", anchor="center")
    treeview.heading("4", text="Quantity")
    treeview.column("4", anchor="center")
    treeview.heading("5", text="Price")
    treeview.column("5", anchor="center")
    treeview.heading("6", text="Price x Quantity")
    treeview.column("6", anchor="center")
    treeview.pack(fill="both")
    
    footFrame = CTkFrame(root, height=100)
    footFrame.pack(fill=X)

    netamountLabel = CTkLabel(footFrame, text="Net Amount : ",font=(fontstyle, 20))
    netamountLabel.place(anchor=W, relx=0.45, rely=0.30)
    priceEntry = StringVar()
    priceEntry.set("0")
    CTkEntry(footFrame, font=(fontstyle, 20, "bold"), state="readonly", textvariable=priceEntry,
          justify="right").place(anchor=W, relx=0.55, rely=0.30)

    cash_image = PhotoImage(file="images/cash_image_2.png")
    payamountButton = CTkButton(footFrame, text="  Checkout", image=cash_image, compound="left",
                             command=checkout, font=(fontstyle, 15))
    payamountButton.place(anchor=W, relx=0.85, rely=0.30)

    binImage = PhotoImage(file="images/bin_image.png")
    deleteitemButton = CTkButton(footFrame, text="  Delete", image=binImage, compound="left", height=20,
                              command=delete_from_tv, font=(fontstyle, 15))
    deleteitemButton.place(anchor=W, relx=0.01, rely=0.16)

    # widgets are get packed and placed in main windows

    headLabel.pack(fill=X)

    productName.place(anchor=W, relx=0.05, rely=0.40)

    codeNumber.place(anchor=W, relx=0.45, rely=0.40)

    searchButton.place(anchor=W, relx=0.85, rely=0.40)

    

   

    

    # keybindings and other main windows attributes
    root.bind("<Shift_L><L>", load_to_memory)
    root.bind("<Shift_L><R>", return_from_memory)
    root.bind("<Shift_L><D>", delete_memory)
    root.bind("<F1>", help_menu)
    root.bind("<Control_L><i>", return_stock)
    root.bind("<Control_L><e>", edit_menu)
    root.bind("<Control_L><a>", add_stock)
    root.bind("<Alt_L><F4>", close_window)
    root.bind("<Control_L><r>", report)
    root.bind("<Control_L><m>", maintain_stock)

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.config(menu=menubar)
    root.mainloop()
    # '''
