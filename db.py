import os
from cs50 import SQL
import sqlite3

# Configure CS50 Library to use SQLite database
DATABASE = "db.db"
SCHEMA = "schema.sql"
DB = None  # Initialize as None to set up later

def main():  
    init_db()
    global DB
    DB = SQL(f"sqlite:///{DATABASE}")  # Initialize DB only after ensuring the database file exists
    

def init_db():
    """Initialize the database with the schema from schema.sql if it doesn't already exist."""
    if not os.path.exists(DATABASE):  # Check if the database file already exists
        with sqlite3.connect(DATABASE) as conn:
            with open(SCHEMA, "r") as f:
                conn.executescript(f.read())  # Executes the entire schema.sql script
        print(f"{DATABASE} created and initialized with schema.sql")


# Database helper functions
def get_username(user_id):
    if DB is None:
        raise RuntimeError("Database has not been initialized.")
    
    result = DB.execute("SELECT username FROM users WHERE id = ?", user_id)
    if result:
        return result[0]['username']
    else:
        return None


def get_fname(user_id):
    if DB is None:
        raise RuntimeError("Database has not been initialized.")
    
    result = DB.execute("SELECT usr_fname FROM user_details WHERE user_id = ?", user_id)
    if result:  # Checks if result is non-empty
        return result[0]['usr_fname']
    else:
        return None  # Or return an empty string "" if preferred


def get_user_roles(user_id):
    if DB is None:
        raise RuntimeError("Database has not been initialized.")
    return DB.execute("SELECT role_name FROM user_roles WHERE user_id = ?", user_id)


def is_admin(user_id):
    roles = get_user_roles(user_id)
    return any(role['role_name'] == 'admin' for role in roles)

def get_reporting_buinesses(user_id):
    return DB.execute("SELECT * FROM businesses WHERE id IN (SELECT business_id FROM user_business_access WHERE user_id = ?)", user_id)

main()