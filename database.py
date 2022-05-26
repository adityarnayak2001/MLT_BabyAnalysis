import sqlite3

class userdbs:
    def __init__(self):
        conn = sqlite3.connect('mlt.db')
        self.c = conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS USERS(user_id integer PRIMARY KEY AUTOINCREMENT,"
                    +"name VARCHAR(30), affiliation VARCHAR(30), number DECIMAL(10),"
                    +"username VARCHAR(40), password VARCHAR(40))")
    
    def validate_username_pass(self,username,password):
        self.c.execute("select * from users where username=\'"+username+"\' and password=\'"+password+"\'")
        rows = self.c.fetchall()
        if(len(rows)):
            return True
        else:
            return False
    
    def registration(self,data):
        self.c.execute("INSERT INTO USERS ('name','affiliation','number','username','password') VALUES" 
        +"(?,?,?,?,?)",(data['name'],data['affiliation'],data['username'],
        data[number],data[username],data[password]))

    def close_connection(self):
        self.conn.close()