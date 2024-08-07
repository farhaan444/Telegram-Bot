import sqlite3
import config


class DB:
    """This class connnects to the databse file and creates a database instance."""

    def __init__(self) -> None:
        self.connection = sqlite3.connect(config.DATABASE_PATH)
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.create_table()
        self.load_default_settings()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def create_table(self):
        """This will create table in the database if table does not exsit already.
        This method will be self call when the DB object is initialized."""
        # users TABLE
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            chat_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                            username TEXT,
                            first_name TEXT,
                            last_name TEXT 
        )
        """)
        # flight_data Table -- ! ON DELETE ACTION on foreign key.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS flight_data(
                            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                            chat_id INTEGER NOT NULL,
                            fly_from TEXT,
                            fly_to TEXT,
                            date_from TEXT,
                            date_to TEXT,
                            nights_in_dst_from TEXT,
                            nights_in_dst_to TEXT,
                            adults INTEGER,
                            curr TEXT,
                            flight_type TEXT,
                            current_price INTEGER,
                            multi_city_req TEXT,
                            FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE CASCADE
        )
        """)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS global_settings(
                            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                            flight_alert_limit INTEGER DEFAULT 0,
                            fs_job_interval INTEGER DEFAULT 900
                            )

        """)
        self.connection.commit()

    def load_default_settings(self):
        check = self.cursor.execute("SELECT COUNT(*) FROM global_settings").fetchone()[0]
        if check == 0:
            self.cursor.execute('INSERT INTO global_settings (id) VALUES (1)')
            self.commit()


    def add_user(self, chat_id, username, first_name, last_name):
        """This method adds a user into the users table"""

        self.cursor.execute('INSERT INTO users (chat_id, username, first_name, last_name) VALUES (?,?,?,?)',
                            (chat_id, username, first_name, last_name,))
        self.commit()

    def del_user(self, chat_id):
        """This method will delete a user from the user database
        This will also delete all flight alert records linked to user in the fligh_data table """
        self.cursor.execute('DELETE FROM users WHERE chat_id =?', (chat_id,))
        self.commit()

    def add_flight_data(self, chat_id, fly_from, fly_to, date_from, date_to, nights_from, nights_to, adults, curr, flight_type, current_price, multi_city_req=None):
        """This method adds all the flight data into the flight_data table"""

        self.cursor.execute('INSERT INTO flight_data (chat_id, fly_from, fly_to, date_from, date_to, nights_in_dst_from, nights_in_dst_to, adults, curr, flight_type, current_price, multi_city_req) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                            (chat_id, fly_from, fly_to, date_from, date_to, nights_from, nights_to, adults, curr, flight_type, current_price, multi_city_req,))
        self.commit()

    def del_flight_data(self, id):
        """This method deletes a row of flight data.
        id parameter is the index of row"""
        self.cursor.execute(
            'DELETE FROM flight_data WHERE id =?', (id,))
        self.commit()

    def del_all_flight_data(self, chat_id):
        """This method will delete all flight data associated with the user"""
        self.cursor.execute(
            'DELETE FROM flight_data WHERE chat_id = ?', (chat_id,))
        self.commit()

    def update_flight_data(self, id, price, data):
        """This method will update data in the flight data table"""
        query = f'UPDATE flight_data SET {data} = ? WHERE id = ?'
        self.cursor.execute(query, (price, id,))
        self.commit()
