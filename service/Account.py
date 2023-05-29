import sqlite3
import os
import hashlib

class AccountObject:
    def __init__(self, id, name:str, password:str, admin:bool):
        self.id = id
        self.name = name
        self.password = password
        self.admin = admin

    def __str__(self):
        return f"AccountObject: {self.id}, {self.name}, {self.admin}"
    
    def __getattribute__(self, name: str):
        return object.__getattribute__(self, name)
    
    def __setattr__(self, name: str, value):
        object.__setattr__(self, name, value)

class AccountService:
    def __init__(self,filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, admin BOOLEAN)"
        cursor.execute(req0)
        connection.commit()
        connection.close()

    def addUser(self,username,password,admin):
        hashPassword = hashlib.sha512(password.encode()).hexdigest()
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO Accounts(username, password, admin) VALUES (?,?,?)"
        cursor.execute(req,(username,hashPassword,admin))
        connection.commit()
        connection.close()

    def logUser(self,username,password):
        hashPassword = hashlib.sha512(password.encode()).hexdigest()
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE username=? AND password=?"
        cursor.execute(req,(username,hashPassword))
        result = cursor.fetchone()
        connection.close()
        if result:
            return AccountObject(result[0],result[1],result[2],result[3])
        else:
            return None
        
    def testIfUsernameExist(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return True
        else:
            return False
        
    def getUser(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return AccountObject(result[0],result[1],result[2],result[3])
        else:
            return None
        
    def getUserById(self,id):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE id=?"
        cursor.execute(req,(id,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return AccountObject(result[0],result[1],result[2],result[3])
        else:
            return None
        
    def deleteUser(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "DELETE FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        connection.commit()
        connection.close()

    def updateUser(self,username,password,admin):
        hashPassword = hashlib.sha512(password.encode()).hexdigest()
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "UPDATE Accounts SET password=?, admin=? WHERE username=?"
        cursor.execute(req,(hashPassword,admin,username))
        connection.commit()
        connection.close()

    def getAllUsers(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts"
        cursor.execute(req)
        result = cursor.fetchall()
        connection.close()
        if result:
            return [AccountObject(r[0],r[1],r[2],r[3]) for r in result]
        else:
            return None
        
    def getAllAdmins(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE admin=1"
        cursor.execute(req)
        result = cursor.fetchall()
        connection.close()
        if result:
            return [AccountObject(r[0],r[1],r[2],r[3]) for r in result]
        else:
            return None
        
    def getAllUsersExceptAdmins(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE admin=0"
        cursor.execute(req)
        result = cursor.fetchall()
        connection.close()
        if result:
            return [AccountObject(r[0],r[1],r[2],r[3]) for r in result]
        else:
            return None
