import sqlite3


class Cash:
    def __init__(self):
        self.con = sqlite3.connect('cash.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Messages`
                    (`mes_id` INTEGER PRIMARY KEY NOT NULL ,
                    `body` VARCHAR(100));
                    ''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Users`
                     (`user_id` INTEGER PRIMARY KEY NOT NULL ,
                     `username` VARCHAR(100));
                     ''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Chats`
                     (`chat_id` INTEGER PRIMARY KEY NOT NULL ,
                     `chatname` VARCHAR(100));
                     ''')

    def check_message(self, mes_id):
        self.cur.execute('SELECT * FROM Messages WHERE mes_id ={0}'.format(mes_id))
        if self.cur.fetchone():
            return True
        else:
            return False

    def add_message(self, mes_id, text):
        self.cur.execute('''INSERT INTO  Messages(mes_id, body) VALUES ('{0}','{1}')'''.format(mes_id, text))
        self.con.commit()
        return

    def check_user(self, user_id):
        self.cur.execute('SELECT * FROM Users WHERE user_id ={0}'.format(user_id))
        ans = self.cur.fetchone()
        if ans:
            return ans[1]
        else:
            return False

    def add_user(self, user_id, username):
        self.cur.execute('''INSERT INTO  Users(user_id, username) VALUES ('{0}','{1}')'''.format(user_id, username))
        self.con.commit()
        return

    def get_user_id(self, username):
        self.cur.execute('SELECT * FROM Users WHERE username ="{0}"'.format(username))
        ans = self.cur.fetchone()
        if ans:
            return ans[0]
        else:
            return False


    def check_chat(self, chat_id):
        self.cur.execute('SELECT * FROM Chats WHERE chat_id ={0}'.format(chat_id))
        ans = self.cur.fetchone()
        if ans:
            return ans[1]
        else:
            return False

    def add_chat(self, chat_id, chatname):
        self.cur.execute('''INSERT OR REPLACE INTO  Chats(chat_id, chatname) VALUES ('{0}','{1}')'''.format(chat_id, chatname))
        self.con.commit()
        return

    def get_chat_id(self, chatname):
        self.cur.execute('SELECT * FROM Chats WHERE chatname ="{0}"'.format(chatname))
        ans = self.cur.fetchone()
        if ans:
            return ans[0]
        else:
            return False
