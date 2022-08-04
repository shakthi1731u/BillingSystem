try:
    import sqlite3
except ModuleNotFoundError:
    print("Required modules are not found")


class DataBase1:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS products
            (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Code_No INTEGER,
                Product_Name TEXT,
                Quantity INTEGER,
                Short_Name TEXT,
                Price INTEGER,
                Product_size TEXT
            )
        """

        self.cur.execute(sql)
        self.con.commit()

    def insert(self, code_no, product_name, quantity, short_name, price, product_size):
        insert_query = """INSERT INTO products
                        (Code_No, Product_Name, Quantity, Short_Name, Price, Product_size) 
                        values(?,?,?,?,?,?)"""

        self.cur.execute(insert_query, (code_no, product_name, quantity, short_name, price, product_size))
        self.con.commit()
        return self.con.close()

    def return_everything(self):
        sql = "SELECT * FROM products"
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.fetchall()

    def return_item(self, search_by, values):
        sql = str
        if search_by == "Code_No":
            sql = "SELECT Code_No, Product_Name, Product_size, Quantity, Price, Id FROM products WHERE Code_No = ?"
        elif search_by == "Product_Name":
            sql = 'SELECT Code_No, Product_Name, Product_size, Quantity, Price, Id FROM products WHERE Product_Name ' \
                  'LIKE "{}%"'.format(values)
            self.cur.execute(sql)
            self.con.commit()
            return self.cur.fetchall()

        self.cur.execute(sql, (values,))
        self.con.commit()
        return self.cur.fetchall()

    def return_for_bill(self, id):
        sql = "SELECT Quantity, Id FROM products WHERE Id = ?"
        self.cur.execute(sql, (id,))
        self.con.commit()
        return self.cur.fetchall()

    def update(self, value, id):
        sql = "UPDATE products SET Quantity = ? WHERE Id = ?"
        self.cur.execute(sql, (value, id))
        self.con.commit()

    def close_con(self):
        self.con.close()

    def return_specific(self, key, word):

        if key == "Code_No":
            sql = "SELECT Code_No, Product_Name,  Short_Name, Quantity, Price, Product_size, Id  FROM products WHERE Code_No = ? ORDER BY Price DESC"
        elif key == "Product_Name":
            sql = "SELECT Code_No, Product_Name,  Short_Name, Quantity, Price, Product_size, Id FROM products WHERE Product_Name LIKE '{}%' ORDER BY Price DESC".format(word)
            self.cur.execute(sql)    
            self.con.commit()
            return self.cur.fetchall()
        elif key == "Product_size":
            sql = "SELECT Code_No, Product_Name,  Short_Name, Quantity, Price, Product_size, Id FROM products WHERE Product_Size LIKE '{}%' ORDER BY Price DESC".format(word)
            self.cur.execute(sql)    
            self.con.commit()
            return self.cur.fetchall()
        

        self.cur.execute(sql, (word, ))    
        self.con.commit()
        return self.cur.fetchall()

    def update_2(self, code_no, product_name, short_name, quantity, price, product_size, id):
        sql = "UPDATE products SET Code_No = ?, Product_Name = ?, Short_Name = ?, Quantity = ?, Price = ?, Product_size = ? WHERE Id = ?"

        self.cur.execute(sql, (code_no, product_name, short_name, quantity, price, product_size, id))
        self.con.commit()
        return True

    def delete_by_id(self, id):
        sql = "DELETE FROM products WHERE Id = ?"

        self.cur.execute(sql, (id, ))
        self.con.commit()
        return True


class TEMP:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS temp
            (
                Id INTEGER,
                Quantity INTEGER
            )
        """

        self.cur.execute(sql)
        self.con.commit()

    def insert_value(self, id, value):
        sql = "INSERT INTO temp VALUES (?, ?)"

        self.cur.execute(sql, (id, value))
        self.con.commit()
        return

    def update(self, quantity, id):
        sql = "UPDATE temp set Quantity = ? WHERE Id = ?"

        self.cur.execute(sql, (quantity, id))
        self.con.commit()
        return

    def return_everything(self):
        sql = "SELECT * FROM temp"

        self.cur.execute(sql)
        self.con.commit()
        return self.cur.fetchall()

    def remove_everything(self):
        sql = "DELETE FROM temp"

        self.cur.execute(sql)
        self.con.commit()
        return

    def remove_particular(self, id):
        sql = "DELETE FROM temp WHERE Id = {}".format(id)

        self.cur.execute(sql)
        self.con.commit()
        return

    def return_specific(self, id):
        sql = "SELECT Quantity FROM temp WHERE Id = ?"

        self.cur.execute(sql, (id,))
        self.con.commit()
        row = self.cur.fetchall()
        row = row[0][0]
        return row


class Bill_no:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS Bill_no
            (
                BILL_NUMBER INTEGER PRIMARY KEY
            )    
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, no):
        sql = "INSERT INTO Bill_no values (?)"

        self.cur.execute(sql, (no,))
        self.con.commit()
        return self.con.close()

    def update(self, no):
        sql = "UPDATE Bill_no SET BILL_NUMBER = ?"

        self.cur.execute(sql, (no,))
        self.con.commit()
        return self.con.close()

    def return_no(self):
        self.cur.execute("SELECT * FROM Bill_no")
        self.con.commit()
        return self.cur.fetchall()


class load_to_memory:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS memory
            (
                sno INTEGER,
                Pro_name TEXT, 
                Size Text, 
                Quan INTEGER,
                Price INTEGER,
                PricexQuan INTEGER,
                Id INTEGER PRIMARY KEY            )
        """

        self.cur.execute(sql)
        self.con.commit()

    def insert(self, sno , name, size, quan, pri, prixquan, id):
        sql = "INSERT INTO memory VALUES(?, ?, ?, ?, ?, ?, ?)"

        self.cur.execute(sql, (sno , name, size, quan, pri, prixquan, id))
        self.con.commit()
        return 

    def check_state(self,):
        sql = "SELECT * FROM memory"

        self.cur.execute(sql)
        self.con.commit()

        size = len(self.cur.fetchall())
        if size >= 1:
             return True
        else:
            return False

    def delete_memory(self):
        sql = "DELETE FROM memory"

        self.cur.execute(sql)
        self.con.commit()
        return    

    def return_everything(self):
        self.cur.execute("SELECT * FROM memory")
        self.con.commit()
        return self.cur.fetchall()


class purchased:
    def __init__(self, db, mon):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = " CREATE TABLE IF NOT EXISTS {} (EARNINGS INTEGER)".format(mon)
    
        self.cur.execute(sql)
        self.con.commit()


    def insert(self, mon, earnings):
        sql = "INSERT INTO {} VALUES ({})".format(mon, earnings)

        self.cur.execute(sql)
        self.con.commit()

        return


    def update(self, mon, earnings):
        sql = "UPDATE {} SET EARNINGS = {}".format(mon, earnings)
     
        self.cur.execute(sql)
        self.con.commit()
        return


    def return_value(self, mon):
        sql = "SELECT * FROM {}".format(mon)

        self.cur.execute(sql)
        self.con.commit()
        return self.cur.fetchall()
        
        
    def check_state(self,mon):
        sql = "SELECT * FROM {}".format(mon)
        
        self.cur.execute(sql)
        self.con.commit()
        
        return True if len(self.cur.fetchall()) >= 1 else False


class Total:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql2 = """
            CREATE TABLE IF NOT EXISTS total
            (
               total_earnings INTEGER,
               total_selled_products INTEGER
            )
        """

        self.cur.execute(sql2)
        self.con.commit()


    def insert(self, total_earnings, total_selled_products):
        sql2 = "INSERT INTO total VALUES (?, ?)"

        self.cur.execute(sql2, (total_earnings, total_selled_products))
        self.con.commit()

        return


    def update(self, total_earnings, total_selled_products):
        sql2 = "UPDATE total SET total_earnings = ?, total_selled_products = ?"

        self.cur.execute(sql2, (total_earnings, total_selled_products))
        self.con.commit()


    def return_value(self):
        sql2 = "SELECT total_earnings, total_selled_products FROM total"

        self.cur.execute(sql2)
        self.con.commit()
        return self.cur.fetchall()
        

    def check_state(self):
        sql2 = "SELECT * FROM total"

        self.cur.execute(sql2)
        self.con.commit() 

        return True if len(self.cur.fetchall()) >= 1 else False


class Return_products:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()


        sql = """CREATE TABLE IF NOT EXISTS return_products
            (
                S_no INTEGER,
                Product TEXT,
                Quan INTEGER,
                Price INTEGER,
                Bill_no INTEGER,
                Id INTEGER,
                Pri_id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        """

        self.cur.execute(sql)
        self.con.commit()

    def insert(self, s_no, product, quan, price, id, bill_no):
        sql = "INSERT INTO return_products(S_no, Product, Quan, Price, Bill_no, Id) VALUES(?, ?, ?, ?, ?, ?)"

        self.cur.execute(sql, (s_no, product, quan, price, bill_no, id))
        self.con.commit()
        return

    def update(self, quantity, pri_id):
        print(quantity)
        sql = "UPDATE return_products SET Quan = ? WHERE Pri_id = ?"
        

        self.cur.execute(sql, (quantity, pri_id))
        self.con.commit()
        return
    
    
    def return_value(self, bill_no):
        sql = "SELECT S_no, Product, Quan, Price, Id, Pri_id FROM return_products WHERE Bill_no = ? ORDER BY S_no ASC"

        self.cur.execute(sql, (bill_no,))
        
        return self.cur.fetchall()


class Return_settings:
    def __init__(self,db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

        sql = """CREATE TABLE IF NOT EXISTS settings
                (
                    Font TEXT,
                    FontSize INTEGER
                )"""

        self.cursor.execute(sql)
        self.connection.commit()


    def insert_default(self):
        self.cursor.execute("SELECT * FROM settings")
        self.connection.commit()
        
        if self.cursor.fetchall() == []:
            sql = "INSERT INTO settings VALUES (?, ?)"
            self.cursor.execute(sql, ("Roboto", 10))
            self.connection.commit()

    def gain_settings(self):
        self.insert_default()
        self.cursor.execute("SELECT * FROM settings")
        self.connection.commit()
        return self.cursor.fetchall()


class User:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

        sql = """CREATE TABLE IF NOT EXISTS users
            (   
                Username TEXT,
                Password TEXT,
                AccessLevel TEXT
            )
        """

        self.cursor.execute(sql)
        self.connection.commit()


    def getallusername(self):
        sql = "SELECT Username FROM users"

        self.cursor.execute(sql)
        self.connection.commit()
        
        return self.cursor.fetchall()[0]


    def insertuser(self, username, password, access):
        sql = "INSERT INTO users VALUES(?, ?, ?)"

        self.cursor.execute(sql, (username, password, access))
        self.connection.commit()
        
        return 


        