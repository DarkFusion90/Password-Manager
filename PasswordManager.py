import sqlite3
import getpass

class PasswordManager:

    def __init__(self):
        self.conn = sqlite3.connect("PasswordDB.db")
        self.cursor = self.conn.cursor()
        self.initTables()

        self.conn.commit()
        self.promptUserActivity()

    def promptUserActivity(self):
        print("Enter your choice:")
        choice = int(input("[1]. Login\n[2]. SignUp\n>>>"))
        if (choice == 1):
            self.userLogin()
        elif (choice == 2):
            self.userSignup()

    def initTables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Users(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                username VARCHAR[50],
                password VARCHER[50],
                e_mail VARCHAR[50],
                SignupDate DATETIME) """)
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Websites(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name VARCHAR[50],
                URL VARCHAR[50],
                Last_Updated TEXT)""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Password (
                websiteID INTEGER,
                userID INTEGER,
                password VARCHAR,
                FOREIGN KEY(websiteID) REFERENCES Websites(ID),
                FOREIGN KEY(userID) REFERENCES Users(ID))""")

    def userLogin(self):
        username = input("Enter your username: ")
        if not self.userExists(username):
            print("The username {} doesn't exists in the database".format(username))
            quit()
        password = getpass.getpass()
        
        loginSuccess = self.attemptLogin(username, password)
        if loginSuccess:
            self.welcomeUser()
        else:
            print("Login Failed. Invalid Username-Password combination.")

    def attemptLogin(self, username, password):
        self.cursor.execute(
            "SELECT password FROM Users WHERE username = ?", (username,))
        actualPass = self.cursor.fetchone()
        return (actualPass[0] == password)
        
    def userExists(self, username):
        self.cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
        return (self.cursor.fetchone() != None)

    def userSignup(self):
        self.newUser()

    def newUser(self):
        email = input("Enter E-mail: ").lower()
        username = input("Enter Username: ")
        password = getpass.getpass()

        self.addUserToDatabase(email, username, password)
        self.conn.commit()
        print("User added successfully!")

    def addUserToDatabase(self, email, username, password):
        self.cursor.execute("""
            INSERT INTO Users(e_mail, username, password) VALUES(?, ?, ?)
            """, (email, username, password))

    def deleteUser(self, userid, username, password):
        pass

    def welcomeUser(self):
        print("Welcome! What would you like to do?")
        print("[1]. Modify/Delete account\n[2]. Add/Remove Password(s)")

PasswordManager()
