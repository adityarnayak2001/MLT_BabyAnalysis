import sqlite3

class userdbs:
    def __init__(self):
        self.conn = sqlite3.connect('mlt.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS USERS(user_id integer PRIMARY KEY AUTOINCREMENT,"
                    +"name VARCHAR(30), affiliation VARCHAR(30), number DECIMAL(10),email VARCHAR(40),"
                    +"username VARCHAR(40), password VARCHAR(40))")
        self.conn.commit()
    
    def validate_username_pass(self,username,password):
        self.c.execute("select password from users where username=\'"+username+"\'")
        rows = self.c.fetchone()
        return rows
    
    def registration(self,data):
        self.c.execute("INSERT INTO USERS ('name','affiliation','number','email','username','password') VALUES" 
        +"(?,?,?,?,?,?)",(data['name'],data['affiliation'],int(data['number']),data['email'],data['username'],data['password']))
        self.conn.commit()
        # print(data)

    def close_connection(self):
        self.conn.close()