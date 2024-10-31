import os
import sqlite3
DATABASE = "kb_teller.db"
test = os.path.exists(DATABASE)

def init_db():
    """Initialize the database with the schema from schema.sql if it doesn't already exist."""
    if not os.path.exists(DATABASE):  # Check if the database file already exists
        print("got here")
        with sqlite3.connect(DATABASE) as conn:
            with open("schema.sql", "r") as f:
                conn.executescript(f.read())  # Executes the entire schema.sql script
        print(f"{DATABASE} created and initialized with schema.sql")

init_db()