try:
    import time
    import win32api
    import database
    import win32print
except ModuleNotFoundError:
    import os
    os.system("batch.bat")

class File_writer:
    def __init__(self, Bill_no, *args, total):
        print(Bill_no)
        obj = database.Bill_no("databases/Bill_no.db")
        if Bill_no == 0:
            bill_no = obj.return_no()
            bill_no = bill_no[0][0]
        else:
            bill_no = Bill_no

        date = time.localtime()

        file = open("files/bill.txt", "w")
        file.writelines("\t    CASH RECEIPT\n")
        file.writelines(f"-------------------------------------\n")
        file.writelines("BILL NO :  {}\n".format(bill_no))
        file.writelines("DATE    :  {} / {} / {}\n".format(date[2], date[1], date[0]))
        file.writelines("-------------------------------------\n")
        file.writelines("PRODUCTS   \t\t PRICE\n")
        file.writelines("-------------------------------------\n")
        for i in args:
            for j in i:
                file.writelines(f"{j[0]:<15}  {j[1]:>12}\n".format())
        file.writelines("-------------------------------------\n")
        file.writelines("TOTAL \t\t\t  {}\n\n".format(total))
        file.writelines("\n\t    THANK YOU!!!\n")

        win32api.ShellExecute(0, "print", "files\\bill.txt", None, ".", 0)

        file.close()
        if Bill_no == 0:
            var = bill_no;var+=1
            obj.update(var)
            return
        else:    
            return


