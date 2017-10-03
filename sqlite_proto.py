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

