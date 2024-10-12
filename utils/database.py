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
        """Commits the current transaction."""
        
        self.connection.commit()

    def close(self):
        """Closes the database connection."""
        
        self.connection.close()

    def create_table(self):
        """
        Creates the database tables if they do not already exist.
        
        The first table is the users table which stores the user's chat_id, username, first_name and last_name.
        
        The second table is the flight_data table which stores all the flight data for each user.
        The table has a foreign key to the users table, which references the users chat_id.
        When a user is deleted from the users table, all their associated flight data will be deleted as well.
        
        The third table is the global_settings table which stores two values:
        flight_alert_limit - the maximum number of flight alerts a user can have
        fs_job_interval - the interval in seconds between each job iteration of the flight search job.
        """
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
        # admin_settings Table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS global_settings(
                            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                            flight_alert_limit INTEGER DEFAULT 0,
                            fs_job_interval INTEGER DEFAULT 900
                            )

        """)
        self.connection.commit()

    def load_default_settings(self):
        """
        This method checks if the global_settings table has any records.
        If not, it inserts a default record with an id of 1.
        This is necessary as the global_settings table is created with a default value of 0, and
        the first time the bot is run, there will be no records in the global_settings table.
        """

        check = self.cursor.execute("SELECT COUNT(*) FROM global_settings").fetchone()[0]
        if check == 0:
            self.cursor.execute('INSERT INTO global_settings (id) VALUES (1)')
            self.commit()


    def add_user(self, chat_id, username, first_name, last_name):
        """
        This method adds a user to the users table.
        The user's chat_id, username, first_name and last_name are stored.
        """

        self.cursor.execute('INSERT INTO users (chat_id, username, first_name, last_name) VALUES (?,?,?,?)',
                            (chat_id, username, first_name, last_name,))
        self.commit()

    def del_user(self, chat_id):
        """
        This method deletes a user from the users table.
        The user's chat_id is required.
        """
        
        self.cursor.execute('DELETE FROM users WHERE chat_id =?', (chat_id,))
        self.commit()

    def add_flight_data(self, chat_id, fly_from, fly_to, date_from, date_to, nights_from, nights_to, adults, curr, flight_type, current_price, multi_city_req=None):
        """
        This method adds a row of flight data to the flight_data table.
        The following parameters are required:
        - chat_id: The user's chat_id.
        - fly_from: The departure airport.
        - fly_to: The destination airport.
        - date_from: The earliest departure date.
        - date_to: The latest departure date.
        - nights_from: The earliest number of nights in the destination.
        - nights_to: The latest number of nights in the destination.
        - adults: The number of adults.
        - curr: The currency.
        - flight_type: The type of flight. E.g. OneWay, Return, MultiCity.
        - current_price: The current price of the flight.
        - multi_city_req: A json formatted string containing the multi-city routes.
        """
       
        self.cursor.execute('INSERT INTO flight_data (chat_id, fly_from, fly_to, date_from, date_to, nights_in_dst_from, nights_in_dst_to, adults, curr, flight_type, current_price, multi_city_req) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                            (chat_id, fly_from, fly_to, date_from, date_to, nights_from, nights_to, adults, curr, flight_type, current_price, multi_city_req,))
        self.commit()

    def del_flight_data(self, id): 
        """
        This method deletes a flight data record from the flight_data table.
        The id of the flight data record is required.
        """

        self.cursor.execute(
            'DELETE FROM flight_data WHERE id =?', (id,))
        self.commit()

    def del_all_flight_data(self, chat_id):
        """
        This method deletes all flight data records from the flight_data table
        for a given user id.
        The user's chat_id is required.
        """

        self.cursor.execute(
            'DELETE FROM flight_data WHERE chat_id = ?', (chat_id,))
        self.commit()

    def update_flight_data(self, id, price, data):
        """
        Updates a flight data record in the flight_data table.
        
        The id of the flight data record is required.
        The price of the flight data record is required.
        The data to be updated is required. This should be a string of the name of the column to be updated.
        
        The method will update the flight data record with the given id, and set the column given in the data parameter to the given price.
        """
        
        query = f'UPDATE flight_data SET {data} = ? WHERE id = ?'
        self.cursor.execute(query, (price, id,))
        self.commit()
