import datetime
import sqlite3
import types

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS investments (user_id, money INTEGER, date timestamp)")

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
        
    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO 'users' ('user_id', 'referrer_id') VALUES (?, ?)", (user_id, referrer_id,))
            else:
                return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
            
    def user_balance(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `balance` FROM users WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return float(result[0][0])

    def count_reeferals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`user_id`) as count FROM `users` WHERE `referrer_id` = ?", (user_id,)).fetchone()[0]

    def user_referal(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `referrer_id` FROM users WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return int(result[0][0]) if result else None

    def set_balance(self, user_id, balance, percent=5):
        refer = self.user_referal(user_id)
        with self.connection:
            if refer:
                self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", ((int(balance) / 100) * percent, refer,))
                self.cursor.execute("UPDATE users SET `balance` = balance + ? WHERE `user_id` = ?", (balance, user_id,))

    def vip(self, user_id, vip):
        with self.connection:
            self.cursor.execute("UPDATE users SET vip = vip + ? WHERE user_id = ?", (vip, user_id,))

    def user_status(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT vip from users where user_id = ?",(user_id,)).fetchone()

    def awaybalance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute("UPDATE users SET `balance` = balance - ? WHERE `user_id` = ?", (balance, user_id,))  

    def add_invest(self, user_id, money):
        with self.connection:
            self.cursor.execute("UPDATE users SET `balance` = balance-? WHERE `user_id` = ?", (money, user_id,))
            return self.cursor.execute("INSERT INTO investments (`user_id`, `money`, `date`) VALUES (?, ?, ?)",
                                       (user_id, money, datetime.datetime.now(),))

    def user_invests(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT user_id, money, date FROM investments WHERE `user_id` = ?", (user_id,)).fetchall()
            return result

    def all_invests(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT SUM(money) FROM investments WHERE `user_id` = {user_id}")
            row = self.cursor.fetchall()
            for rows in row:
                print(row[0][0])
                if row[0][0] == None:
                    return 0
                else:
                    return row[0][0]

    def dell_invests(self, user_id):
        with self.connection:
            result = self.cursor.execute("DELETE FROM investments WHERE `user_id` = ?", (user_id,)).fetchall()
            return result

    def add_pl(self, user_id, amount, bid):
        with self.connection:
            result = self.cursor.execute("INSERT INTO orders (`user_id`, `amount`, `numb`) VALUES (?, ?, ?)", (user_id, amount, bid))
            return result
    
    def check_id(self):
        with self.connection:
            result = self.cursor.execute("SELECT numb FROM orders ORDER BY id DESC LIMIT 1").fetchone()
            return result

    def check_pl(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM orders WHERE `user_id` = {user_id} ORDER BY numb DESC LIMIT 1").fetchall()
            return result

    def check_adm(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT admin FROM users WHERE `user_id` = {user_id}").fetchall()
            return result[0][0]
        
    def check_vip(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT vip FROM users WHERE `user_id` = {user_id}").fetchall()
            return result[0][0]

    def new_bal(self, user_id, balance):
        with self.connection:
            result = self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (user_id, balance,)).fetchall()
            return result
        
    def checkstats(self, balance, user_id):
        with self.connection:
            balanceStats = self.cursor.execute(f"SELECT balance FROM users `user_id` = ?", (balance,))

