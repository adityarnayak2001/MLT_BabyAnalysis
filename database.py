import sqlite3

class userdbs:
    def __init__(self):
        conn = sqlite3.connect('mlt.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXITS USERS(user_id integer PRIMARY KEY AUTOINCREMENT,"
                    +"name VARCHAR(30), affiliation VARCHAR(30), number DECIMAL(10)"
                    +"username VARCHAR(40), password VARCHAR(40), )")
    
    def validate_username_pass(username,password):
        print()
    
    def registration():
        c.execute("INSERT INTO USERS ('username','password') VALUES ('aditya@gmail.com','aditya')")

print('command executed succesfully')
conn.commit()
conn.close()