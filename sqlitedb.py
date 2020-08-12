import sqlite3


class UsersDataBase:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def check_table(self):
        """Checking if table exists"""
        with self.connection:
            self.cursor.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'""")
            return self.cursor.fetchone()[0]

    def create_table(self):
        """Creating table, if it's not exists"""
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                       full_name VARCHAR(255) NOT NULL,
                                       date DATE NOT NULL,
                                       sex CHAR(1) NOT NULL
                                        )""")

    def clear_table(self):
        """Clearing all data"""
        with self.connection:
            self.cursor.execute("""DELETE FROM users""")
            return self.cursor.rowcount

    def add_user(self, full_name, date_of_birth, sex):
        """Adding user to DataBase"""
        with self.connection:
            return self.cursor.execute("""INSERT INTO users (full_name, date, sex) 
                                        VALUES (?, ?, ?)""",
                                       (full_name, date_of_birth, sex))

    def unique_full_name_date(self):
        """Getting users with unique fullname + date"""
        with self.connection:
            return self.cursor.execute("""SELECT * FROM users GROUP BY full_name, date ORDER BY full_name""").fetchall()

    def insert_million_rows(self, params):
        """Getting users with unique fullname + date"""
        with self.connection:
            for chunk in params:
                self.cursor.execute("""INSERT INTO users(full_name, date, sex) 
                                            VALUES (?, ?, ?)""", chunk)

    def get_m_starts_f(self):
        """Getting men with full name starts 'F'"""
        with self.connection:
            return self.cursor.execute("""SELECT full_name FROM users WHERE sex = 'm' AND full_name LIKE 'F%'""").fetchall()

