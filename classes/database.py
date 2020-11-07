# Description
# It's very upsetting when the data about registered users disappears after the program is completed. 
# To avoid this problem, you need to create a database 
# where you will store all the necessary information about the created credit cards. 
# We will use SQLite to create the database.
# SQLite is a database engine. It is software that allows users to interact with a relational database. 
# In SQLite, a database is stored in a single file — a trait that distinguishes it from other database engines. 
# This allows for greater accessibility: copying a database is no more complicated than copying the file that stores the data, 
# and sharing a database implies just sending an email attachment.
# You can use the sqlite3 module to manage SQLite database from Python. 
# You don't need to install this module. It is included in the standard library.
# To use the module, you must first create a Connection object that represents the database. 
# Here the data will be stored in the example.s3db file:
#   import sqlite3
#   conn = sqlite3.connect('example.s3db')
# Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL queries:
#   cur = conn.cursor()
# Executes some SQL query
#   cur.execute('SOME SQL QUERY')
# After doing some changes in DB don't forget to commit them!
#   conn.commit()
# To get data returned by SELECT query you can use fetchone(), fetchall() methods:
#   cur.execute('SOME SELECT QUERY')
# Returns the first row from the response
#   cur.fetchone()
# Returns all rows from the response
#   cur.fetchall()
#
# Instruction
# In this stage, create a database named card.s3db with a table titled card. It should have the following columns:
#   id INTEGER
#   number TEXT
#   pin TEXT
#   balance INTEGER DEFAULT 0
# Pay attention: your database file should be created when the program starts, 
# if it hasn’t yet been created. And all created cards should be stored in the database from now.
# Do not forget to commit your DB changes right after executing a query!
# 
# Example
# The symbol > represents the user input. 
# Notice that it's not a part of the input.
# 1. Create an account
# 2. Log into account
# 0. Exit
# >1
#
# Your card has been created
# Your card number:
# 4000003429795087
# Your card PIN:
# 6826
#
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
#
# Enter your card number:
# >4000003429795087
# Enter your PIN:
# >4444
#
# Wrong card number or PIN!
#
# 1. Create an account
# 2. Log into account
# 0. Exit
# >2
#
# Enter your card number:
# >4000003429795087
# Enter your PIN:
# >6826
#
# You have successfully logged in!
#
# 1. Balance
# 2. Log out
# 0. Exit
# >1
#
# Balance: 0
#
# 1. Balance
# 2. Log out
# 0. Exit
# >2
#
# You have successfully logged out!
#
# 1. Create an account
# 2. Log into account
# 0. Exit
# >0
#
# Bye!

import constants
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self):
        self.message_delimiter = "--------------------------------------------------------------------"
        self.db_file = constants.DATABASE_FILE
        self.connection = None
        self.verbose = False

    def print_version_message(self):
        """Print the SQLite version on a successful connection to the database file."""
        print(self.message_delimiter)
        print("Running SQLite version:", sqlite3.version)

    def print_table_create_success_message(self, table_name):
        """Print a success message if a table was created successfully."""
        print(self.message_delimiter)
        print(f">> Table `{table_name}` created successfully\n")

    def print_record_add_success_message(self, id, table_name):
        """Print a success message if a record was added to a table successfully."""
        print(self.message_delimiter)
        print(f">> ID {id} added successfully to table `{table_name}`")
        print(self.message_delimiter)

    def create_connection(self):
        """Create a database connection to a SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_file)
        
            if self.verbose:
                self.print_version_message()
        except Error as e:
            print(e)

    def connect(self):
        """Create a table if the connection is successful."""
        self.create_connection()
        if self.connection is not None:
            self.create_card_table()
        else:
            print("Error: cannot create the database connection.")

    def disconnect(self):
        """Disconnects from a database connection."""
        if self.connection:
            self.connection.close()

    def get_create_default_card_table_sql(self):
        """Return the default SQL to create the card table."""
        return ''' CREATE TABLE IF NOT EXISTS card (
                                    id integer PRIMARY KEY,
                                    number text NOT NULL,
                                    pin text NOT NULL,
                                    balance integer default 0
                                ); '''

    def create_card_table(self, create_card_table_sql=""):
        """Create the card table.

        Arguments:
            create_card_table_sql -- a create table statement
        """
        try:
            cur = self.connection.cursor()
            if create_card_table_sql == "":
                create_card_table_sql = self.get_create_default_card_table_sql()
            cur.execute(create_card_table_sql)
        
            if self.verbose:
                self.print_table_create_success_message("card")
        except Error as e:
            print(e)

    def get_default_insert_card_sql(self):
        """Return the default SQL to insert a new card into the card table."""
        return ''' INSERT INTO card(number,pin,balance)
                VALUES(?,?,?) '''

    def create_card_record(self, data, insert_card_sql=""):
        """Create a database card record.

        Arguments:
            data -- the card data
            insert_card_sql -- an insert into table statement
        """
        if insert_card_sql == "":
            insert_card_sql = self.get_default_insert_card_sql()
        cur = self.connection.cursor()
        cur.execute(insert_card_sql, data)
        self.connection.commit()
        
        if self.verbose:
            self.print_record_add_success_message(cur.lastrowid, "card")

    def get_update_card_sql(self):
        """Return the default SQL to update a card into the card table."""
        return ''' UPDATE card
                SET number = ? ,
                    pin = ? ,
                    balance = ?
                WHERE id = ?'''

    def update_card_record(self, data, update_card_sql=""):
        """Update a database card record.

        Arguments:
            data -- the card data containing updated values
            connection -- the database connection
        """
        if update_card_sql == "":
            update_card_sql = self.get_update_card_sql()
        cur = self.connection.cursor()
        cur.execute(update_card_sql, data)
        self.connection.commit()

    def get_delete_card_sql(self):
        """Return the default SQL to delete a card from the card table by card id."""
        return 'DELETE FROM card WHERE id=?'

    def delete_card_record(self, card_id, delete_card_sql=""):
        """Delete a database card record by id.

        Arguments:
            card_id -- the card record id
            connection -- the database connection
        """
        if delete_card_sql == "":
            delete_card_sql = self.get_delete_card_sql()
        cur = self.connection.cursor()
        cur.execute(delete_card_sql, (card_id,))
        self.connection.commit()

    def get_card_data_by_number(self, number):
        """Return the card data based on the given card number.

        Arguments:
            number -- the card number

        Returns:
            The card data if number found, or None
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM card WHERE number=?", (number,))
        return cur.fetchone()

    def get_card_data_by_id(self, card_id):
        """Return the card data based on the given card id.

        Arguments:
            card_id -- the card id

        Returns:
            The card data if the id exists, or None
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM card WHERE id=?", (card_id,))
        return cur.fetchone()